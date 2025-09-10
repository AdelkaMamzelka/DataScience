#!/usr/bin/env python3

def data_types():
    int_var = 10
    str_var = "Hello"
    float_var = 10.5
    bool_var = True
    list_var = [1, 2, 3]
    dict_var = {'key': 'value'}
    tuple_var = (1, 2)
    set_var = {1, 2, 3}

    types_list = [type(int_var), type(str_var), type(float_var), type(bool_var), type(list_var), type(dict_var), type(tuple_var), type(set_var)]
    
    print('[' + ', '.join([t.__name__ for t in types_list]) + ']')

if __name__ == '__main__':
    data_types()
    