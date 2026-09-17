import asyncio
import datetime
import logging
import xml.etree.ElementTree as ET

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class NetScopeCoordinator(DataUpdateCoordinator):
    """Coordinator to poll network via nmap and parse details."""

    def __init__(self, hass, target_subnet):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=datetime.timedelta(minutes=5),
        )
        self.target_subnet = target_subnet

    async def _async_update_data(self):
        """Run nmap scan asynchronously and parse XML results."""
        try:
            # Run nmap with ping scan (-sn) and XML output (-oX -)
            cmd = ["nmap", "-sn", "-oX", "-", self.target_subnet]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise UpdateFailed(f"Nmap scan failed: {stderr.decode().strip()}")

            return self._parse_nmap_xml(stdout.decode())

        except Exception as err:
            raise UpdateFailed(f"Error executing nmap scan: {err}")

    def _parse_nmap_xml(self, xml_data):
        """Parse Nmap XML output to extract IP, MAC, Vendor, and Hostname."""
        devices = {}
        try:
            root = ET.fromstring(xml_data)
            for host in root.findall("host"):
                status = host.find("status")
                if status is not None and status.get("state") == "up":
                    ip_address = None
                    mac_address = None
                    vendor = "Unknown"
                    hostname = "Unknown"

                    # Get IP and MAC addresses
                    for addr in host.findall("address"):
                        if addr.get("addrtype") == "ipv4":
                            ip_address = addr.get("addr")
                        elif addr.get("addrtype") == "mac":
                            mac_address = addr.get("addr")
                            vendor = addr.get("vendor", "Unknown")

                    # Get Hostname
                    hnames = host.find("hostnames")
                    if hnames is not None:
                        hn_elem = hnames.find("hostname")
                        if hn_elem is not None:
                            hostname = hn_elem.get("name", "Unknown")

                    if ip_address:
                        device_id = mac_address if mac_address else ip_address
                        devices[device_id] = {
                            "ip": ip_address,
                            "mac": mac_address,
                            "vendor": vendor,
                            "hostname": hostname if hostname != "Unknown" else ip_address,
                        }
        except ET.ParseError as e:
            _LOGGER.error("Failed to parse Nmap XML output: %s", e)

        return devices
