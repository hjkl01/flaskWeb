def test_view():
    with open('ping_nmap_result.txt', 'r') as file:
        con = file.readlines()
    temp = '</br>'.join(con).replace(
        'False', '<span style="color: red">False</span>').replace(
            'error', '<span style="color: red">error</span>')
    result = '%s<br>%s' % (len(con), temp)
    return result
