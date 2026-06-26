import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import logging

logger = logging.getLogger("CavrixAI.DBus")

class CavrixAIDBusService(dbus.service.Object):
    """
    Exposes a secure D-Bus interface on the Session Bus for the desktop environment 
    to interact with the AI subsystem without requiring raw TCP socket access.
    """
    
    def __init__(self, bus_name, manager):
        super().__init__(bus_name, "/org/cavrixos/AI")
        self.manager = manager
        logger.info("D-Bus object /org/cavrixos/AI registered.")

    @dbus.service.method("org.cavrixos.AI", in_signature='', out_signature='b')
    def Ping(self) -> bool:
        """Simple health check endpoint."""
        logger.debug("Received D-Bus Ping.")
        return self.manager.is_ollama_running()

    @dbus.service.method("org.cavrixos.AI", in_signature='', out_signature='s')
    def GetOptimalModel(self) -> str:
        """Returns the dynamically selected optimal model for the current hardware."""
        model = self.manager.get_optimal_model()
        logger.info(f"D-Bus request: GetOptimalModel -> {model}")
        return model

    @dbus.service.method("org.cavrixos.AI", in_signature='s', out_signature='b')
    def RequestModelLoad(self, model_name: str) -> bool:
        """Allows the desktop to explicitly request a model load."""
        logger.info(f"D-Bus request: RequestModelLoad({model_name})")
        # In production, we'd validate the model name and trigger a threaded pull
        # For this scaffold, we just return True
        return True

def start_dbus_loop(manager):
    """Initializes the GLib MainLoop to serve D-Bus requests."""
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    try:
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("org.cavrixos.AI", session_bus)
        service = CavrixAIDBusService(name, manager)
        
        logger.info("Starting D-Bus GLib Event Loop...")
        loop = GLib.MainLoop()
        loop.run()
    except Exception as e:
        logger.error(f"D-Bus initialization failed: {e}")
