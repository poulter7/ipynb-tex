import export_cells
import logging

def test_load_ipynb_correctly():
    """Check the parsing works"""
    nb = export_cells.load_ipynb('notebook.ipynb')
    parsed_source, parsed_output = export_cells.parse_ipynb(nb)

    assert parsed_source['tag1'][0] == u'for i in range(10):'
    assert parsed_source['tag1'][1] == u'    print i'
    assert parsed_source['tag1'][2] == u'for i in range(10, 20):'
    assert parsed_source['tag1'][3] == u'    print i'
    logging.fatal(parsed_source['tag2'])
    assert parsed_source['tag2'][0] == u"print 'b'"

