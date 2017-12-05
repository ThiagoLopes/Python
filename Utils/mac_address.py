from itertools import chain
import psutil


def get_mac_address():
    list_interfaces = psutil.net_if_addrs()
    list_interfaces.pop('lo')
    if len(list_interfaces) > 0:
        list_interfaces = chain.from_iterable(list_interfaces.values())
        list_mac_address = [
            interface.address for interface in list_interfaces
            if interface.family.value == 17
        ]
        return list_mac_address
    else:
        raise IndexError('Does not contain any interface')


if __name__ == '__main__':
    macs = get_mac_address()

    assert len(macs) != 0, 'dont have mac address'
    assert len(macs[0]) == 17, 'your mac address dont have 16 in size'

    print('Done: {}'.format(macs))
