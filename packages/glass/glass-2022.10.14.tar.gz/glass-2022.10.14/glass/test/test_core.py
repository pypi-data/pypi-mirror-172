import pytest


def test_generator_error():

    from glass.core import generate, GeneratorError, State

    def mygenerator():
        for n in range(5):
            if n == 3:
                raise ZeroDivisionError
            yield

    g = mygenerator()

    with pytest.raises(GeneratorError, match='iteration 3: ') as exc_info:
        for state in generate([g]):
            pass

    e = exc_info.value
    assert type(e.__cause__) == ZeroDivisionError
    assert e.generator is g
    assert isinstance(e.state, State)


def test_generate():

    from unittest.mock import Mock
    from glass.core import generate, State

    g = Mock()
    g.__name__ = 'generator'
    g.receives = None
    g.yields = 'alphabet'
    g.send.side_effect = [None, 'abc', 'def', StopIteration]

    # yields state
    gen = generate([g])

    state = next(gen)
    assert isinstance(state, State)
    assert state['alphabet'] == 'abc'

    state = next(gen)
    assert state['alphabet'] == 'def'

    with pytest.raises(StopIteration):
        next(gen)

    # reset
    g.send.side_effect = [None, 'abc', 'def', StopIteration]

    # yields variable
    gen = generate([g], 'alphabet')

    alphabet = next(gen)
    assert alphabet == 'abc'

    alphabet = next(gen)
    assert alphabet == 'def'

    with pytest.raises(StopIteration):
        next(gen)


def test_group():

    from unittest.mock import Mock
    from glass.core import group

    generator = Mock()
    generator.__name__ = 'foo'
    generator.receives = None
    generator.yields = 'bar'

    g = group('test', [generator])

    assert g.receives == 'state'
    assert g.yields == 'test'

    generator.send.return_value = None

    state = g.send(None)

    assert generator.send.called
    assert generator.send.call_args.args == (None,)

    generator.send.return_value = object()

    state = g.send(None)

    assert generator.send.call_count == 2
    assert generator.send.call_args.args == (None,)
    assert state['bar'] is generator.send.return_value

    g.close()

    assert generator.close.called


def test_save_load(tmp_path):

    from glass.core import save, load

    # also test appending of .glass suffix, so not given here
    filename = tmp_path / 'test'

    g = save(filename, ['var_a', 'var_b', 'var_c'])

    assert g.receives == ('var_a', 'var_b', 'var_c')
    assert g.yields is None

    # prime generator
    g.send(None)

    # send values: ITER, var_a, var_b, var_c
    g.send(('a', 'b', 'c'))
    g.send(('A', 'B', 'C'))

    # done
    g.close()

    assert (tmp_path / 'test.glass').exists()

    g = load(filename)

    assert g.receives is None
    assert g.yields == ('var_a', 'var_b', 'var_c')

    # prime generator
    g.send(None)

    # load values: var_a, var_b, var_c
    assert g.send(None) == ('a', 'b', 'c')
    assert g.send(None) == ('A', 'B', 'C')

    # end of iteration
    with pytest.raises(StopIteration):
        g.send(None)
