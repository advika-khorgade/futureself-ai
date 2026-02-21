"""Authentication manager."""
import bcrypt
from datetime import datetime
from .database import User, get_session
import re


class AuthManager:
    """Manages user authentication."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Validate password strength.
        Returns (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        return True, ""
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
        """
        Register a new user.
        Returns (success, message)
        """
        session = get_session()
        
        try:
            # Validate inputs
            if len(username) < 3:
                return False, "Username must be at least 3 characters long"
            
            if not AuthManager.validate_email(email):
                return False, "Invalid email format"
            
            is_valid, error_msg = AuthManager.validate_password(password)
            if not is_valid:
                return False, error_msg
            
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    return False, "Username already exists"
                else:
                    return False, "Email already registered"
            
            # Create new user
            password_hash = AuthManager.hash_password(password)
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash
            )
            
            session.add(new_user)
            session.commit()
            
            return True, "Registration successful!"
            
        except Exception as e:
            session.rollback()
            return False, f"Registration failed: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, str, dict]:
        """
        Login a user.
        Returns (success, message, user_data)
        """
        session = get_session()
        
        try:
            # Find user
            user = session.query(User).filter(User.username == username).first()
            
            if not user:
                return False, "Invalid username or password", {}
            
            # Verify password
            if not AuthManager.verify_password(password, user.password_hash):
                return False, "Invalid username or password", {}
            
            # Update last login
            user.last_login = datetime.utcnow()
            session.commit()
            
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
                "last_login": user.last_login
            }
            
            return True, "Login successful!", user_data
            
        except Exception as e:
            return False, f"Login failed: {str(e)}", {}
        finally:
            session.close()
