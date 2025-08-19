import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime


class SASEmailService:
    """Email service that uses SAS configuration file for email settings"""
    
    def __init__(self, sas_config_path: Optional[str] = None):
        # Default SAS config path
        if sas_config_path is None:
            sas_config_path = "/opt/sas/config/Lev1/SASApp/sasv9.cfg"
        
        self.sas_config_path = sas_config_path
        self.config = self._load_config()
        
        # Load email template
        self.email_template = self._load_email_template()
        
        # Fallback settings if SAS config is not available
        self.fallback_smtp_server = os.getenv('SMTP_SERVER', 'localhost')
        self.fallback_smtp_port = int(os.getenv('SMTP_PORT', '25'))
        self.fallback_from_email = os.getenv('FROM_EMAIL', 'bhanu.prathap.gaddam@tn.gov')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL', 'bhanu.prathap.gaddam@tn.gov')
    
    def _load_config(self):
        """Load SAS email configuration"""
        try:
            if os.path.exists(self.sas_config_path):
                config = self._load_sas_email_config(self.sas_config_path)
                print(f"✅ Loaded SAS email configuration from {self.sas_config_path}")
                return config
            else:
                print(f"⚠️ SAS config file not found at {self.sas_config_path}, using fallback settings")
                return {}
        except Exception as e:
            print(f"⚠️ Error loading SAS config: {e}, using fallback settings")
            return {}
    
    def _load_sas_email_config(self, cfg_path):
        """
        Parse SAS config file to extract email settings.
        Example options in sasv9.cfg:
            -EMAILSYS SMTP
            -EMAILHOST smtp.example.com
            -EMAILPORT 25
            -EMAILID user@example.com
        """
        config = {}
        pattern = re.compile(r"^-(EMAIL\w+)\s+(.*)", re.IGNORECASE)

        with open(cfg_path, "r") as f:
            for line in f:
                line = line.strip()
                match = pattern.match(line)
                if match:
                    key, value = match.groups()
                    config[key.upper()] = value

        return config
    
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
    
    def get_smtp_settings(self):
        """Get SMTP settings from SAS config or fallback"""
        smtp_server = self.config.get('EMAILHOST', self.fallback_smtp_server)
        smtp_port = int(self.config.get('EMAILPORT', self.fallback_smtp_port))
        from_email = self.config.get('EMAILID', self.fallback_from_email)
        
        return {
            'server': smtp_server,
            'port': smtp_port,
            'from_email': from_email,
            'system': self.config.get('EMAILSYS', 'SMTP')
        }
    
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
            # Use provided email or fallback to notification email
            recipient_email = to_email or self.notification_email
            if not recipient_email:
                print(f"⚠️ No recipient email configured for mr_dv alert: {record_id}")
                return False
            
            # Get SMTP settings
            smtp_settings = self.get_smtp_settings()
            
            # Create email content
            subject = "Medical Record Request"
            body = self._create_email_body(record_id, patient_name, facility_name)
            
            # Send email
            return self._send_email(recipient_email, subject, body, smtp_settings)
            
        except Exception as e:
            print(f"❌ Error sending mr_dv notification email: {e}")
            return False
    
    def _create_email_body(self, record_id: str, patient_name: Optional[str] = None,
                          facility_name: Optional[str] = None) -> str:
        """Create the email body for mr_dv notification using loaded HSB template"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Start with the loaded template
        body = self.email_template + "\n\n"
        
        # Add record details
        body += f"Record Details:\n"
        body += f"- Record ID: {record_id}\n"
        body += f"- Timestamp: {timestamp}\n"
        
        if patient_name:
            body += f"- Patient: {patient_name}\n"
        
        if facility_name:
            body += f"- Facility: {facility_name}\n"
        
        body += f"\nTennessee Department of Health\n"
        body += f"Bhanu Prathap Gaddam\n"
        body += f"bhanu.prathap.gaddam@tn.gov"
        
        return body
    
    def _send_email(self, to_email: str, subject: str, body: str, smtp_settings: dict) -> bool:
        """
        Send email using SMTP with SAS configuration
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body text
            smtp_settings: SMTP configuration dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = smtp_settings['from_email']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session and send
            with smtplib.SMTP(smtp_settings['server'], smtp_settings['port']) as server:
                # Send the message
                server.send_message(msg)
                
            print(f"✅ SAS email notification sent to {to_email} for record: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send SAS email to {to_email}: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test the SAS SMTP configuration"""
        try:
            smtp_settings = self.get_smtp_settings()
            
            print(f"Testing SAS SMTP connection to {smtp_settings['server']}:{smtp_settings['port']}")
            
            with smtplib.SMTP(smtp_settings['server'], smtp_settings['port']) as server:
                status = server.noop()[0]
                if status == 250:
                    print("✅ SAS SMTP connection test successful")
                    return True
                else:
                    print(f"⚠️ SAS SMTP connection test returned status: {status}")
                    return False
                    
        except Exception as e:
            print(f"❌ SAS SMTP connection test failed: {e}")
            return False