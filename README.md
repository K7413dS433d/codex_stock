To install a custom app in **Frappe ERPNext** while in **production mode**, follow these steps:

### **1. Enable Maintenance Mode**
Since you're in production mode, you should first enable maintenance mode to prevent disruptions:

```bash
bench --site yoursite set-maintenance-mode on
```

### **2. SSH into Your Server**
Connect to your server via SSH if you haven't already:

```bash
ssh user@yourserver
```

### **3. Navigate to Your Bench Directory**
Move to the directory where your ERPNext instance is installed:

```bash
cd /path/to/your/bench
```

### **4. Get the Custom App**
If your custom app is hosted on GitHub or another Git repository, clone it into the `apps` directory:

```bash
cd apps
git clone https://github.com/yourusername/yourcustomapp.git
```

### **5. Install the App in Bench**
Once the app is in the `apps` directory, return to the main `bench` directory and run:

```bash
bench setup requirements
bench get-app yourcustomapp
bench --site yoursite install-app yourcustomapp
```

### **6. Build and Restart Bench**
Now, build assets and restart Frappe:

```bash
bench build
bench restart
```

### **7. Migrate and Clear Cache**
Apply any necessary migrations:

```bash
bench --site yoursite migrate
bench --site yoursite clear-cache
```

### **8. Disable Maintenance Mode**
Once the installation is complete, disable maintenance mode:

```bash
bench --site yoursite set-maintenance-mode off
```

Your custom app should now be successfully installed in your production ERPNext environment! Let me know if you run into any issues.