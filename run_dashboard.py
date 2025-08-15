#!/usr/bin/env python
"""
Dashboard Launcher for Medicos
Automatically detects Flask availability and runs appropriate dashboard version
"""

import sys
import subprocess
import os

def check_flask_installed():
    """Check if Flask is installed"""
    try:
        import flask
        import dateutil
        return True
    except ImportError:
        return False

def install_flask():
    """Try to install Flask and dependencies"""
    print("🔧 Installing Flask and dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "python-dateutil"])
        print("✅ Flask installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Flask: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False

def run_flask_dashboard():
    """Run the full Flask dashboard"""
    print("🚀 Starting Full Flask Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    
    try:
        os.chdir('app')
        subprocess.run([sys.executable, "dashboard_server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running Flask dashboard: {e}")

def run_simple_dashboard():
    """Run the simple built-in dashboard"""
    print("🚀 Starting Simple Dashboard (No Flask)...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    
    try:
        os.chdir('app')
        subprocess.run([sys.executable, "simple_dashboard.py"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running simple dashboard: {e}")

def main():
    """Main launcher function"""
    print("🎯 Medicos Dashboard Launcher")
    print("=" * 40)
    
    # Check if Flask is available
    flask_available = check_flask_installed()
    
    if flask_available:
        print("✅ Flask detected - using full dashboard with advanced features")
        print("🔄 Starting in 2 seconds... (Press Ctrl+C to cancel)")
        try:
            import time
            time.sleep(2)
            run_flask_dashboard()
        except KeyboardInterrupt:
            print("\n🛑 Cancelled by user")
    else:
        print("⚠️ Flask not found - offering options...")
        print("\nOptions:")
        print("  1. Install Flask for full dashboard features")
        print("  2. Use simple dashboard (built-in, limited features)")
        print("  3. Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1":
                    if install_flask():
                        print("🎉 Flask installed! Restarting with full dashboard...")
                        run_flask_dashboard()
                    else:
                        print("⚠️ Flask installation failed. Using simple dashboard...")
                        run_simple_dashboard()
                    break
                    
                elif choice == "2":
                    run_simple_dashboard()
                    break
                    
                elif choice == "3":
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Cancelled by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break

if __name__ == "__main__":
    main()