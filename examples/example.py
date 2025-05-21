"""
Example script demonstrating the use of HermesInspector to interact with a React Native app.
"""

import asyncio
import logging
import json
import sys
import os
import time

# Add the parent directory to the path so we can import the react_native_client package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hermes_inspector import HermesInspector

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    # Replace with your device's IP address or use localhost for local development
    DEVICE_IP = "localhost"
    METRO_PORT = 8081
    
    logger.info(f"Connecting to React Native app's Hermes debugger at {DEVICE_IP}:{METRO_PORT}")
    
    # Create an inspector instance
    inspector = HermesInspector(DEVICE_IP, METRO_PORT)
    
    try:
        # Connect to the app with increased timeout
        success, message = inspector.connect(timeout=30)
        logger.info(f"Connection status: {success}, Message: {message}")
        
        if not success:
            logger.error("Failed to connect to the app. Make sure the app is running with debugging enabled and Metro bundler is running.")
            return
        
        # Get the UI tree with increased timeout
        logger.info("Getting UI tree...")
        ui_tree = inspector.get_ui_tree(timeout=30)
        
        if ui_tree:
            if isinstance(ui_tree, dict) and "error" in ui_tree:
                logger.error(f"Failed to get UI tree: {ui_tree['error']}")
            else:
                logger.info("UI Tree retrieved successfully")
                
                # # Step 1: Tap on some stock tickers
                # stocks = ["AAPL", "MSFT", "AMZN"]
                
                # for stock in stocks:
                #     logger.info(f"Attempting to tap on {stock}...")
                #     success, message = inspector.tap_element(text=stock, timeout=30)
                #     logger.info(f"Tap result for {stock}: {success}, Message: {message}")
                #     time.sleep(1)  # Wait a bit between taps
                
                # # Step 2: Try scrolling down to see more stocks
                # logger.info("Scrolling down to see more stocks...")
                # success, message = inspector.scroll(direction="down", distance=300, timeout=30)
                # logger.info(f"Scroll result: {success}, Message: {message}")
                

                # Step 5: Try scrolling back up
                logger.info("Scrolling back up...")
                success, message = inspector.scroll(direction="up", distance=300, timeout=30)
                logger.info(f"Scroll result: {success}, Message: {message}")
                time.sleep(1)  # Wait a bit
                                # Step 3: Get UI tree again after scrolling
                logger.info("Scrolling down to see more stocks...")
                success, message = inspector.scroll(direction="down", distance=400, timeout=30)
                logger.info(f"Scroll result: {success}, Message: {message}")
                time.sleep(1)
                
                
                                # Step 4: Try tapping on elements that might be visible after scrolling
                more_stocks =  ["JPM"]
                
                for stock in more_stocks:
                    logger.info(f"Attempting to tap on {stock} (after scrolling)...")
                    success, message = inspector.tap_element(text=stock, timeout=30)
                    logger.info(f"Tap result for {stock}: {success}, Message: {message}")
                    time.sleep(1)  # Wait a bit between taps
                
                logger.info("Getting UI tree after scrolling...")
                ui_tree_after_scroll = inspector.get_ui_tree(timeout=30)
                print(ui_tree_after_scroll)
                logger.info("Trying horizontal scrolling (left)...")
                time.sleep(1)
                success, message = inspector.scroll(direction="up", distance=200, timeout=30)
                logger.info(f"Horizontal scroll result: {success}, Message: {message}")
                time.sleep(1)
                success, message = inspector.tap_element(text='1D', timeout=30)
                logger.info(f"Tap result for index: {success}, Message: {message}")
                time.sleep(1)
                success, message = inspector.tap_element(text='1M', timeout=30)
                logger.info(f"Tap result for index: {success}, Message: {message}")
                time.sleep(1)
                success, message = inspector.tap_element(text='1Y', timeout=30)
                logger.info(f"Tap result for index: {success}, Message: {message}")
        else:
            logger.warning("Failed to get UI tree")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        # Close the connection
        logger.info("Closing connection...")
        inspector.close()
        logger.info("Connection closed")

if __name__ == "__main__":
    asyncio.run(main())
