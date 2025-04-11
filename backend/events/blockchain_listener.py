import threading
import time
import json
import logging
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('BlockchainListener')

class BlockchainListener:
    """
    Listens for events emitted by the blockchain network and triggers appropriate actions.
    
    This class implements a background thread that continuously listens for events
    from the Hyperledger Fabric network, such as anomaly detection events, and
    processes them accordingly.
    """
    
    def __init__(self, callback=None):
        """
        Initialize the blockchain listener.
        
        Args:
            callback (function, optional): A callback function to be called when an event is received.
                                          The callback should accept an event object as its argument.
        """
        self.callback = callback
        self.event_queue = Queue()
        self.running = False
        self.listener_thread = None
        self.event_processor_thread = None
    
    def start(self):
        """
        Start the blockchain listener.
        """
        if self.running:
            logger.warning("Blockchain listener is already running.")
            return
        
        self.running = True
        
        # Start the listener thread
        self.listener_thread = threading.Thread(target=self._listen_for_events)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        
        # Start the event processor thread
        self.event_processor_thread = threading.Thread(target=self._process_events)
        self.event_processor_thread.daemon = True
        self.event_processor_thread.start()
        
        logger.info("Blockchain listener started.")
    
    def stop(self):
        """
        Stop the blockchain listener.
        """
        if not self.running:
            logger.warning("Blockchain listener is not running.")
            return
        
        self.running = False
        
        # Wait for threads to terminate
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=5)
        
        if self.event_processor_thread and self.event_processor_thread.is_alive():
            self.event_processor_thread.join(timeout=5)
        
        logger.info("Blockchain listener stopped.")
    
    def _listen_for_events(self):
        """
        Background thread that listens for events from the blockchain network.
        
        In a real implementation, this would use the Hyperledger Fabric SDK to
        register event listeners for specific chaincode events.
        """
        logger.info("Event listener thread started.")
        
        # Mock implementation for demonstration purposes
        # In a real implementation, this would use the Hyperledger Fabric SDK
        while self.running:
            try:
                # Simulate receiving events from the blockchain
                # This is just a placeholder for the actual event listening logic
                time.sleep(10)  # Check for events every 10 seconds
                
                # Mock event data (for demonstration)
                # In a real implementation, this would be actual events from the blockchain
                mock_events = self._get_mock_events()
                
                # Add events to the queue
                for event in mock_events:
                    self.event_queue.put(event)
                    logger.debug(f"Added event to queue: {event['event_type']}")
            
            except Exception as e:
                logger.error(f"Error in event listener: {str(e)}")
                time.sleep(5)  # Wait before retrying
        
        logger.info("Event listener thread stopped.")
    
    def _process_events(self):
        """
        Background thread that processes events from the queue.
        """
        logger.info("Event processor thread started.")
        
        while self.running:
            try:
                # Get an event from the queue (with timeout to allow checking running flag)
                try:
                    event = self.event_queue.get(timeout=1)
                except:
                    continue
                
                # Process the event
                logger.info(f"Processing event: {event['event_type']}")
                
                # Call the callback function if provided
                if self.callback:
                    try:
                        self.callback(event)
                    except Exception as e:
                        logger.error(f"Error in event callback: {str(e)}")
                
                # Mark the event as processed
                self.event_queue.task_done()
            
            except Exception as e:
                logger.error(f"Error in event processor: {str(e)}")
                time.sleep(1)  # Wait before retrying
        
        logger.info("Event processor thread stopped.")
    
    def _get_mock_events(self):
        """
        Generate mock events for demonstration purposes.
        
        In a real implementation, this would be replaced by actual events from the blockchain.
        
        Returns:
            list: A list of mock events.
        """
        # This is just for demonstration
        # In a real implementation, this would be actual events from the blockchain
        return []
    
    def register_callback(self, callback):
        """
        Register a callback function to be called when an event is received.
        
        Args:
            callback (function): A function that accepts an event object as its argument.
        """
        self.callback = callback
    
    def add_event(self, event):
        """
        Add an event to the queue for processing.
        
        This method can be used to manually add events to the queue for testing or
        to simulate events from the blockchain.
        
        Args:
            event (dict): The event to add to the queue.
        """
        self.event_queue.put(event)
        logger.debug(f"Manually added event to queue: {event['event_type']}")


class AnomalyEventHandler:
    """
    Handles anomaly events from the blockchain network.
    
    This class provides methods for processing anomaly detection events
    and triggering appropriate actions, such as sending notifications.
    """
    
    def __init__(self, notification_service=None):
        """
        Initialize the anomaly event handler.
        
        Args:
            notification_service: A service for sending notifications.
        """
        self.notification_service = notification_service
    
    def handle_event(self, event):
        """
        Handle an anomaly event.
        
        Args:
            event (dict): The event to handle.
        """
        if event['event_type'] == 'AnomalyDetected':
            logger.info(f"Handling anomaly event: {event['id']}")
            
            # Extract event data
            anomaly_id = event.get('id')
            organization_id = event.get('organizationId')
            data_type = event.get('dataType')
            anomaly_score = event.get('anomalyScore')
            
            # Log the anomaly
            logger.info(f"Anomaly detected: ID={anomaly_id}, Org={organization_id}, Type={data_type}, Score={anomaly_score}")
            
            # Send notification if notification service is available
            if self.notification_service:
                self.notification_service.send_notification(
                    recipient=organization_id,
                    subject="Anomaly Detected",
                    message=f"An anomaly has been detected in your {data_type} data with a score of {anomaly_score}."
                )
            
            # Additional processing can be added here
            # For example, triggering an investigation workflow
        
        else:
            logger.warning(f"Unknown event type: {event['event_type']}")


class NotificationService:
    """
    Provides methods for sending notifications to users.
    
    This is a mock implementation for demonstration purposes.
    In a real implementation, this would integrate with an email service,
    SMS gateway, or other notification mechanism.
    """
    
    def __init__(self):
        """
        Initialize the notification service.
        """
        self.notifications = []  # Store notifications for demonstration
    
    def send_notification(self, recipient, subject, message):
        """
        Send a notification to a recipient.
        
        Args:
            recipient (str): The recipient of the notification.
            subject (str): The subject of the notification.
            message (str): The message content.
            
        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        # This is just a mock implementation
        # In a real implementation, this would send an actual notification
        notification = {
            'recipient': recipient,
            'subject': subject,
            'message': message,
            'timestamp': time.time()
        }
        
        self.notifications.append(notification)
        logger.info(f"Notification sent to {recipient}: {subject}")
        
        return True
    
    def get_notifications(self, recipient=None):
        """
        Get notifications for a specific recipient or all notifications.
        
        Args:
            recipient (str, optional): The recipient to filter by. If None, returns all notifications.
            
        Returns:
            list: A list of notifications.
        """
        if recipient:
            return [n for n in self.notifications if n['recipient'] == recipient]
        else:
            return self.notifications