def initialise_desc(desc):
    for key in desc:
        desc[key] = None

reg_desc = {
    'esp': None,
    'ebp': None,
    'eax': None,
    'ebx': None,
    'ecx': None,
    'edx': None,
    'esi': None,
    'edi': None,
}


addr_desc = {}