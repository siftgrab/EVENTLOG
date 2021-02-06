#! /usr/bin/env python3
# Extract Common Windows Events that contain information about file objects processes creation
# from the Security.evtx log file
# 
# Requires Python-evtx https://github.com/williballenthin/python-evtx
# and BeautifulSoup
# Event IDs can be added or removed by editing the "evtxs" variable

import re
import mmap
import contextlib

import argparse
from bs4 import BeautifulSoup, element

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view

evtxs = {1102: 'Log Cleared',
4688: 'Process Created',
4689: 'Process Exited',
4690: 'Attempt to Duplicate Object Handle',
4656: 'Request to Access to Object Handle',
4658: 'Handle to an Object was Closed',
4661: 'Handle to an Object was Requested',
4662: 'Operation was performed o an Object',
4663: 'Attempted Access a File or Object',
4670: 'Permission to File or Object Changed',
4673: 'Attempted Access of Privileged Service',
4674: 'Operation attempted on a privileged service',
4658: 'Access to a File or object closed',
4697: 'New Service has been Installed',
4782: 'Account Password Hash was Accessed', 
5140: 'Network Share Accessed',
5156: 'Program Connected to another process', 
5158: 'Filter allowed bind to local port'
}

event_info_names = ('Date',
'EventID',
'Description',
'Computer'
)

event_data_names = (
'LogonType',
'AuthenticationPackageName',
'LmPackageName',
'LogonProcessName',
'SubjectUserSID',
'IpAddress',
'IpPort',
'WorkstationName',
'SubjectUserSid',
'SubjectUserName',
'SubjectDomainName',
'SubjectLogonId',
'TargetUserSid',
'TargetUserName',
'TargetDomainName',
'TargetLogonId',
'LogonGuid',
'TransmittedServices',
'KeyLength',
'ProcessName',
'ProcessId',
'NewProcessId',
'NewProcessName',
'ParentProcessName',
'CommandLine',
'TokenElevationType')

def main():
    parser = argparse.ArgumentParser(description=
        "Extract Windows Account Logon Events to CSV")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows Security EVTX event log file")
    parser.add_argument('-n', '--NoHeader', action='store_true', help="Do not print header")
    parser.add_argument('-f', '--Filter', action='store_true', help="Apply a filter to suppress service manager events")
    parser.add_argument('-i', '--Include', type = lambda s: re.split('[ ,;]', s),
        help="Print lines containing a single string or comma separated list of strings")
    parser.add_argument('-x','--Exclude', type = lambda s: re.split('[ ,;]', s), 
        help="Print lines containing a single string or comma separated list of strings")
    
    args = parser.parse_args()

    excludes = (args.Exclude)
    includes = (args.Include)
    
    with open(args.evtx, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0,
                                          access=mmap.ACCESS_READ)) as buf:
            fh = FileHeader(buf, 0x0)
            if not args.NoHeader:
                print(','.join(map(str,event_info_names + event_data_names)))
            for xml, record in evtx_file_xml_view(fh):
                soup = BeautifulSoup(xml, "lxml")
                Date = soup.event.system.timecreated['systemtime']
                Date = Date[:-7]
                EventID = int(soup.event.system.eventid.string)
                Computer = soup.event.system.computer.string               
                if EventID in evtxs:
                    event_info = "%s,%s,%s,%s," % (Date,EventID,evtxs[EventID],Computer)

                    try:
                        event_data = {}
                        for child in soup.eventdata.children:
                            if type(child) is element.Tag:
                                event_data[child['name']] = ' '.join(child.text.split())
                        event_data_result = []
                        for value in event_data_names:
                            result = event_data.get(value)
                            if result is None:
                                result = ''
                            event_data_result.append(result)
                    except:
                        pass
                    try:
                        e = "00000000000003e"
                        f = "services.exe"
                        g = "svchost.exe"
                              
                        a = ((event_info) + ','.join(map(str,event_data_result)))
                        if args.Filter:
                            if a.casefold().find(e) == -1:
                                if a.casefold().find(f) == -1:
                                    print(a)                                
                                elif a.casefold().find(g) == -1:
                                    print(a)
                        else:
                            print(a)
                        if args.Exclude:
                            print(yes)
                            for term in exclusions:
                                print(term)
                                if a.casefold().find(term):
                                    noprint='yes'
                            if not noprint:
                                print(a)
                        if args.Include:
                            print(yes)
                            for term in inclusions:
                                print(term)
                                if a.casefold().find(term):
                                    noprint='yes'
                            if not noprint:
                                print(a)
                    except:
                        pass
if __name__ == "__main__":
    main()