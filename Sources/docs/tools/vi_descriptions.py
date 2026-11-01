"""Read only the uncompressed STRG description in modern LabVIEW RSRC files.

No VI is executed or rewritten. Unsupported layouts fail explicitly.
Format reference: MIT-licensed pylabview (Mefistotelis), LVrsrcontainer.py / LVblock.py.
This small reader intentionally does not interpret compiled code or panel heaps.
"""
from pathlib import Path
import struct


def description(path: Path) -> str:
    data = path.read_bytes()

    def u32(offset: int) -> int:
        if offset < 0 or offset + 4 > len(data):
            raise ValueError(f'{path}: truncated resource table')
        return struct.unpack_from('>I', data, offset)[0]

    if data[:6] != b'RSRC\r\n' or data[8:12] not in (b'LVIN', b'LVCC'):
        raise ValueError(f'{path}: unsupported VI container')
    info, payload = u32(16), u32(24)
    table = info + u32(info + 44)
    count = u32(table) + 1
    if count > 4096:
        raise ValueError(f'{path}: unsupported resource count')
    for index in range(count):
        header = table + 4 + index * 12
        if data[header:header + 4] != b'STRG':
            continue
        if u32(header + 4) != 0:
            raise ValueError(f'{path}: multiple STRG sections unsupported')
        section = table + u32(header + 8)
        start = payload + u32(section + 12)
        size = u32(start)
        length = u32(start + 4)
        if size != length + 4 or start + 4 + size > len(data):
            raise ValueError(f'{path}: compressed or unsupported STRG')
        text = data[start + 8:start + 8 + length]
        if b'\x00' in text:
            raise ValueError(f'{path}: Unicode STRG requires an explicit decoder')
        return text.decode('cp1252').replace('\r\n', '\n').replace('\r', '\n')
    return ''
