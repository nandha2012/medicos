import os
import sys
import re
from typing import Optional, Dict, Any
from datetime import datetime

# Try to import win32 modules for Outlook integration
try:
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False
    print("⚠️ win32com not available. Install with: pip install pywin32")

# Fallback SMTP imports
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    SMTP_AVAILABLE = True
except ImportError:
    SMTP_AVAILABLE = False


class EmailService:
    def __init__(self, use_outlook=True):
        # Load configuration from SASS file
        self.config = self._load_sass_config()
        
        self.use_outlook = (use_outlook and OUTLOOK_AVAILABLE and 
                           self.config.get('use-outlook', True))
        
        # Load email template
        self.email_template = self._load_email_template()
        
        # Configuration from SASS or fallback to environment variables
        self.from_email = self.config.get('sender', os.getenv('FROM_EMAIL', 'noreply@medicos.com'))
        self.notification_email = self.config.get('notification-email', os.getenv('NOTIFICATION_EMAIL'))
        self.email_subject = self.config.get('subject', 'Medical Record Request')
        
        # SMTP fallback settings
        smtp_config = self.config.get('smtp-fallback', {})
        self.smtp_server = smtp_config.get('server', os.getenv('SMTP_SERVER', 'localhost'))
        self.smtp_port = smtp_config.get('port', int(os.getenv('SMTP_PORT', '587')))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        
        # Initialize Outlook if available
        self.outlook = None
        if self.use_outlook:
            try:
                self.outlook = win32com.client.Dispatch("Outlook.Application")
                print("✅ Connected to local Outlook application")
            except Exception as e:
                print(f"⚠️ Could not connect to Outlook: {e}")
                print("Falling back to SMTP method")
                self.use_outlook = False
    
    def _load_sass_config(self) -> Dict[str, Any]:
        """Load email configuration from SASS file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'email_config.sass')
            config_path = os.path.abspath(config_path)
            
            if not os.path.exists(config_path):
                print(f"⚠️ SASS config file not found at {config_path}, using defaults")
                return {}
            
            config = {}
            with open(config_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Simple SASS parser for the email settings map
                settings_match = re.search(r'\$email-settings:\s*\((.*?)\)', content, re.DOTALL)
                if settings_match:
                    settings_content = settings_match.group(1)
                    
                    # Parse key-value pairs
                    for line in settings_content.split('\n'):
                        line = line.strip()
                        if ':' in line and not line.startswith('//'):
                            # Handle nested maps like smtp-fallback
                            if '(' in line:
                                key = line.split(':')[0].strip()
                                nested_content = re.search(r'\((.*?)\)', line, re.DOTALL)
                                if nested_content:
                                    nested_map = {}
                                    for nested_line in nested_content.group(1).split(','):
                                        if ':' in nested_line:
                                            nested_key, nested_value = nested_line.split(':', 1)
                                            nested_key = nested_key.strip()
                                            nested_value = nested_value.strip().strip('"').strip("'")
                                            if nested_value.isdigit():
                                                nested_value = int(nested_value)
                                            nested_map[nested_key] = nested_value
                                    config[key] = nested_map
                            else:
                                key, value = line.split(':', 1)
                                key = key.strip()
                                value = value.strip().rstrip(',').strip('"').strip("'")
                                if value.lower() == 'true':
                                    value = True
                                elif value.lower() == 'false':
                                    value = False
                                config[key] = value
            
            print(f"✅ Loaded email configuration from SASS file")
            return config
            
        except Exception as e:
            print(f"⚠️ Error loading SASS config: {e}, using defaults")
            return {}
    
    def _load_email_template(self) -> str:
        """Load email template from HSB file"""
        try:
            template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'email_body.hsb')
            template_path = os.path.abspath(template_path)
            
            if not os.path.exists(template_path):
                print(f"⚠️ HSB template file not found at {template_path}, using default")
                return self._get_default_template()
            
            with open(template_path, 'r', encoding='utf-8') as file:
                template = file.read().strip()
                
            print(f"✅ Loaded email template from HSB file")
            return template
            
        except Exception as e:
            print(f"⚠️ Error loading HSB template: {e}, using default")
            return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """Default email template if HSB file is not available"""
        return """Hello,

Thank you for assisting the Tennessee Department of Health in our public health efforts to conduct surveillance on hepatitis C virus positive women and their infants. Please reach out if you have any questions or concerns.

Kind regards,"""
        
    def send_mr_dv_notification(self, record_id: str, patient_name: Optional[str] = None, 
                               facility_name: Optional[str] = None, 
                               to_email: Optional[str] = None) -> bool:
        """
        Send email notification when mr_dv is not equal to 1
        
        Args:
            record_id: The record identifier
            patient_name: Optional patient name
            facility_name: Optional facility name
            to_email: Email address to send to (defaults to env variable)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not to_email:
                to_email = self.notification_email
                if not to_email:
                    print(f"⚠️ No notification email configured for mr_dv alert: {record_id}")
                    return False
            
            # Use the configured subject
            subject = self.email_subject
            
            # Use the loaded template
            body = self._create_email_body_from_template(record_id, patient_name, facility_name)
            
            # Send email using appropriate method
            if self.use_outlook and self.outlook:
                return self._send_outlook_email(to_email, subject, body)
            elif SMTP_AVAILABLE:
                return self._send_smtp_email(to_email, subject, body)
            else:
                print("❌ No email sending method available (neither Outlook nor SMTP)")
                return False
            
        except Exception as e:
            print(f"❌ Error sending mr_dv notification email: {e}")
            return False
    
    def _create_email_body_from_template(self, record_id: str, patient_name: Optional[str] = None,
                                       facility_name: Optional[str] = None) -> str:
        """Create the email body using the loaded HSB template"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Start with the template
        body = self.email_template + "\n\n"
        
        # Add record details
        body += f"Record ID: {record_id}\n"
        body += f"Timestamp: {timestamp}\n"
        
        if patient_name:
            body += f"Patient: {patient_name}\n"
        
        if facility_name:
            body += f"Facility: {facility_name}\n"
        
        body += "\nTennessee Department of Health\n"
        body += "Bhanu Prathap Gaddam\n"
        body += "bhanu.prathap.gaddam@tn.gov"
        
        return body
    
    def _send_outlook_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send email using local Outlook application
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body text
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a new mail item
            mail = self.outlook.CreateItem(0)  # 0 is olMailItem
            
            # Set email properties
            mail.To = to_email
            mail.Subject = subject
            mail.Body = body
            
            # Set the sender if configured
            if self.from_email:
                mail.SentOnBehalfOfName = self.from_email
            
            # Send the email
            mail.Send()
            
            print(f"✅ Outlook email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send Outlook email to {to_email}: {e}")
            return False
    
    def _send_smtp_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send email using SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body text
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Enable TLS if credentials are provided
                if self.smtp_username and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                
                # Send email
                server.send_message(msg)
                
            print(f"✅ Email notification sent to {to_email} for record: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False