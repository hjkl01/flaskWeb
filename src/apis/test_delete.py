import os


async def test_delete():
    os.system('rm ping_nmap_result.txt')
    return 'delete ping_nmap_result.txt success !'
