from helloworld import say_hello

def test_helloworld_no_params(name=None):
    assert say_hello() == "hello world"

    

def test_helloworld():
    assert say_hello("vinayak") == "hello vinayak"
    
    

