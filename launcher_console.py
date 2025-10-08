import subprocess
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 60)
    print(" " * 15 + "YourVision Launcher")
    print(" " * 10 + "Computer Vision Games & Tools")
    print("=" * 60)
    print()

def main():
    apps = [
        {
            "name": "BlurFace",
            "file": "BlurFace.py",
            "description": "Privacy tool - detect and blur faces in real-time"
        },
        {
            "name": "HandMouse",
            "file": "HandMouse.py",
            "description": "Control mouse using hand gestures"
        },
        {
            "name": "DanceWithMe",
            "file": "DanceWithMe.py",
            "description": "Dance moves mimicked by a stickman"
        },
        {
            "name": "FoodEater",
            "file": "FoodEater.py",
            "description": "Eat foods by opening your mouth"
        },
        {
            "name": "MyAvatar",
            "file": "MyAvatar.py",
            "description": "Create cartoonized or stylized avatars"
        },
        {
            "name": "Red Light Green Light",
            "file": "Red_Light_Green_Light.py",
            "description": "Squid Game inspired movement game"
        }
    ]
    
    while True:
        print_header()
        
        # Display menu
        for i, app in enumerate(apps, 1):
            print(f"{i}. {app['name']}")
            print(f"   {app['description']}")
            print()
        
        print(f"{len(apps) + 1}. Exit")
        print()
        print("=" * 60)
        
        try:
            choice = input("\nEnter your choice (1-{}): ".format(len(apps) + 1))
            
            if not choice.isdigit():
                print("\n❌ Invalid choice! Please enter a number.")
                input("\nPress Enter to continue...")
                continue
            
            choice = int(choice)
            
            if choice == len(apps) + 1:
                print("\n👋 Thank you for using YourVision!")
                break
            
            if 1 <= choice <= len(apps):
                selected_app = apps[choice - 1]
                
                # Check if file exists
                if not os.path.exists(selected_app["file"]):
                    print(f"\n❌ Error: {selected_app['file']} not found!")
                    print("Make sure all .py files are in the same directory.")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"\n🚀 Launching {selected_app['name']}...")
                print("💡 Tip: Close the application window to return to this menu.")
                print()
                
                # Launch the application
                try:
                    if sys.platform == "win32":
                        subprocess.run([sys.executable, selected_app["file"]])
                    else:
                        subprocess.run([sys.executable, selected_app["file"]])
                    
                    print(f"\n✅ {selected_app['name']} closed.")
                except Exception as e:
                    print(f"\n❌ Error launching {selected_app['name']}: {e}")
                
                input("\nPress Enter to continue...")
            else:
                print(f"\n❌ Invalid choice! Please enter a number between 1 and {len(apps) + 1}.")
                input("\nPress Enter to continue...")
                
        except ValueError:
            print("\n❌ Invalid input! Please enter a number.")
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using YourVision!")
            break

if __name__ == "__main__":
    main()