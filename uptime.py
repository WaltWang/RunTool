import os
import socket
import time
import ntplib

__author__ = "Wang MingJun"


def gettimestr(ts=time.time()):
    return time.strftime("%Y-%m-%d %X", time.localtime(ts))


class NTPClient:
    """NTP client session."""

    def __init__(self):
        """Constructor."""
        pass

    def request(self, host, version=2, port='ntp', timeout=5):
        """Query a NTP server.

        Parameters:
        host    -- server name/address
        version -- NTP version to use
        port    -- server port
        timeout -- timeout on socket operations

        Returns:
        NTPStats object
        """
        # lookup server address
        addrinfo = socket.getaddrinfo(host, port)[0]
        family, sockaddr = addrinfo[0], addrinfo[4]

        # create the socket
        s = socket.socket(family, socket.SOCK_DGRAM)

        try:
            s.settimeout(timeout)

            # create the request packet - mode 3 is client
            query_packet = ntplib.NTPPacket(mode=3, version=version,
                                            tx_timestamp=ntplib.system_to_ntp_time(time.time()))

            # send the request
            s.sendto(query_packet.to_data(), sockaddr)

            # wait for the response - check the source address
            src_addr = None,
            while src_addr[0] != sockaddr[0]:
                response_packet, src_addr = s.recvfrom(256)

            # build the destination timestamp
            dest_timestamp = ntplib.system_to_ntp_time(time.time())
        except socket.timeout:
            # raise TPException("No response received from %s." % host)
            return
        except socket.error:
            # raise TPException("No response received from %s." % host)
            return
        finally:
            s.close()

        # construct corresponding statistics
        stats = ntplib.NTPStats()
        stats.from_data(response_packet)
        stats.dest_timestamp = dest_timestamp

        return stats


def getnpttime(addr='ntp.api.bz'):
    c = NTPClient()
    response = c.request(addr)
    if response:
        return response.tx_time


def setostime(ts):
    # _date = time.strftime('%Y-%m-%d', time.localtime(ts))
    # _time = time.strftime('%X', time.localtime(ts))
    # os.system('date {} && time {}'.format(_date, _time))
    os.system(time.strftime('date %Y-%m-%d && time %X', time.localtime(ts)))


def upostime(addr='ntp.api.bz'):
    c = NTPClient()
    response = c.request(addr)
    if response:
        ts = response.tx_time
        setostime(ts)
        print("NTP Time:", gettimestr(ts))
        print("local Time:", gettimestr())
    else:
        print("NTP [%s] NoGet" % addr)


if __name__ == '__main__':
    import sys
    defntp = 's1a.time.edu.cn'

    if len(sys.argv) > 1:
        upostime(sys.argv[1])
    else:
        upostime(defntp)
