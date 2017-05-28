
from ..base.renderer import BaseRenderer

class AirOS(BaseRenderer):

    def cleanup(self, output):
        stripped = [
                a.strip() for a in output.splitlines() if a.strip()
                ]
        return '\n'.join(stripped)


class SystemRenderer(AirOS):
    """
    Write configuration for
    - resolv
    - system
    - users
    """

    def _get_resolv(self):
        dns_server = self.config.get('dns_servers', [])
        return {
                'nameserver' : reversed(list(enumerate(dns_server))),
        }

    def _get_system(self):
        general = self.config.get('general', {}).copy()
        if general:
            general['timezone'] = general.get('timezone', 'UTC')
            general['latitude'] = general.get('latitude', '')
            general['longitude'] = general.get('longitude', '')
            general['timestamp'] = general.get('timestamp','')
            general['reset'] = general.get('reset', 'enabled')

        return general

    
class NetworkRenderer(AirOS):
    """
    Write configuration for
    - bridge
    - vlan
    """

    def _get_bridge(self):
        interfaces = self.config.get('interfaces', [])
        bridge_def = [
                i for i in interfaces if i['type'] == 'bridge'
                ]
        return reversed(list(enumerate(bridge_def)))

    def _get_vlan(self):
        interfaces = self.config.get('interfaces', [])
        vlan_def = [
                i for i in interfaces if '.' in i['name']
                ]

        airos_vlan = []

        for v in vlan_def:
            airos_v = v.copy()
            airos_v['devname'] = v['name'].split('.')[0]
            airos_v['id'] = v['name'].split('.')[1]
            airos_v['status'] = "enabled" if not v['disabled'] else "disabled"
            airos_vlan.append(airos_v)

        return enumerate(airos_vlan)