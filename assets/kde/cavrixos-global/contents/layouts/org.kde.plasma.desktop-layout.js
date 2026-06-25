// CavrixOS Custom Desktop Layout (Mac-like)
// Designed for KDE Plasma 6

// Clear all default panels (removes the Windows-style bottom taskbar)
var panels = panelIds;
for (var i = 0; i < panels.length; ++i) {
    var panel = panelById(panels[i]);
    if (panel) {
        panel.remove();
    }
}

// 1. Create Top Bar (Mac-style Menu Bar)
var topPanel = new Panel;
topPanel.location = "top";
topPanel.height = 30;
topPanel.alignment = "center";
topPanel.hiding = "none";
topPanel.floating = false;

// Add widgets to Top Bar
topPanel.addWidget("org.kde.plasma.kickoff"); // Application Launcher (Apple Logo replacement)
topPanel.addWidget("org.kde.plasma.appmenu"); // Global Menu
var spacer = topPanel.addWidget("org.kde.plasma.panelspacer");
spacer.currentConfigGroup = ["Configuration", "General"];
spacer.writeConfig("expanding", true);
topPanel.addWidget("org.kde.plasma.digitalclock"); // Clock in center or right
var spacer2 = topPanel.addWidget("org.kde.plasma.panelspacer");
spacer2.currentConfigGroup = ["Configuration", "General"];
spacer2.writeConfig("expanding", true);
topPanel.addWidget("org.kde.plasma.systemtray"); // System Tray (Wifi, Bluetooth, etc)

// 2. Create Bottom Floating Dock
var dock = new Panel;
dock.location = "bottom";
dock.height = 56;
dock.alignment = "center";
dock.hiding = "none";
// In Plasma 6, setting the length mode and floating creates the Mac Dock effect
dock.lengthMode = "fit";
dock.floating = true;

// Add widgets to Dock
var taskManager = dock.addWidget("org.kde.plasma.icontasks");
taskManager.currentConfigGroup = ["Configuration", "General"];
taskManager.writeConfig("launchers", [
    "applications:cavrix-welcome.desktop",
    "applications:org.kde.dolphin.desktop",
    "applications:org.kde.konsole.desktop",
    "applications:systemsettings.desktop"
]);
dock.addWidget("org.kde.plasma.marginsseparator");
dock.addWidget("org.kde.plasma.trash");
