def rd_wr_module(path_dict, input_dict=None, mode='r'):
    """ Utility for reading/writing from/to txt. format file lists data type. This module can work in two modes
    (read - 'r' and write - 'r').
    
    :param path_dict: path to file for reading/writing (enable for r/w modes).
    :param input_dict: list for writing (enable only for w mode).
    :param mode: select mode of module operation.
    :return: list or None. In read mode - list got from file. In write mode - None.
    """
    with path_dict.open(mode=mode) as reader:
        if mode == 'r':
            txt_content = reader.readlines()
            return [elements.replace('\n', '') for elements in txt_content]
        elif mode == 'w' or mode == 'a':
            for word in input_dict:
                reader.write(f'%s\n' % word)
