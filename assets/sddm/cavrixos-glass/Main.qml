import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import SddmComponents 2.0

Rectangle {
    id: root
    width: Screen.width
    height: Screen.height
    color: "#09090B"

    // Background Image
    Image {
        id: bg
        anchors.fill: parent
        source: "/usr/share/backgrounds/cavrixos/login-wallpaper.png"
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
    }

    // Glassmorphism Login Panel
    Rectangle {
        id: loginPanel
        width: 400
        height: 500
        anchors.centerIn: parent
        color: Qt.rgba(0.066, 0.094, 0.152, 0.4) // Surface #111827 with 40% opacity
        radius: 20
        border.color: Qt.rgba(0.215, 0.254, 0.317, 0.5) // Border #374151
        border.width: 1

        layer.enabled: true
        layer.effect: GaussianBlur {
            radius: 32
            samples: 64
            transparentBorder: true
        }
    }

    // Login Content
    Item {
        anchors.fill: loginPanel
        
        Image {
            id: logo
            source: "/usr/share/pixmaps/cavrixos-logo.svg"
            width: 80
            height: 80
            anchors.top: parent.top
            anchors.topMargin: 40
            anchors.horizontalCenter: parent.horizontalCenter
            smooth: true
            antialiasing: true
        }

        Text {
            id: timeText
            anchors.top: logo.bottom
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
            text: Qt.formatTime(new Date(), "hh:mm")
            font.family: "Inter"
            font.pixelSize: 48
            font.weight: Font.Bold
            color: "#F8FAFC"
        }
        
        // Timer to update clock
        Timer {
            interval: 1000
            running: true
            repeat: true
            onTriggered: timeText.text = Qt.formatTime(new Date(), "hh:mm")
        }

        TextField {
            id: passwordField
            width: 300
            height: 50
            anchors.bottom: loginButton.top
            anchors.bottomMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
            placeholderText: "Password"
            echoMode: TextInput.Password
            font.family: "Inter"
            font.pixelSize: 16
            color: "#F8FAFC"
            background: Rectangle {
                color: Qt.rgba(0.121, 0.160, 0.215, 0.5) // Elevated Surface #1F2937
                radius: 10
                border.color: passwordField.activeFocus ? "#06B6D4" : "transparent"
                border.width: 1
            }
            onAccepted: sddm.login(userModel.lastUser, passwordField.text, sessionModel.lastIndex)
        }

        Button {
            id: loginButton
            width: 300
            height: 50
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 40
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Login"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.DemiBold
            
            background: Rectangle {
                color: loginButton.down ? "#1D4ED8" : "#2563EB" // Primary/Secondary
                radius: 10
            }
            contentItem: Text {
                text: loginButton.text
                font: loginButton.font
                color: "#F8FAFC"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onClicked: sddm.login(userModel.lastUser, passwordField.text, sessionModel.lastIndex)
        }
    }
}
