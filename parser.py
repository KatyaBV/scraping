import winappdbg
#from winappdbg import win32
import re
s = winappdbg.System()
s.request_debug_privileges()
s.scan_processes()
file = input("File name:")
print("[+]Started parsing")
for p, path in s.find_processes_by_filename(file):
    pid = p.get_pid()
    bits = p.get_bits()
    print("pid = ", pid, ", ", bits, "bits")
    mmap = p.get_memory_map()
    mapf = p.get_mapped_filenames(mmap)
    for m in mmap:
        a = m.BaseAddress
        fn = mapf.get(a, None)
        if m.has_content():
            print(" address 0x%x size 0 x%x state 0 x%x protect 0x%x type 0 x%x[% s ]" % (a, m.RegionSize, m.State, m.Protect, m.Type, fn))
            d = p.read(a, m.RegionSize)
            cc = re.findall("\d{4}-\d{4}-\d{4}-\d{4}", d[::2])
            if len ( cc ) > 0:
                print(cc)
                input()



