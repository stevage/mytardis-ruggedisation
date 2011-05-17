from django.template import Library
from tardis_portal.models import ExperimentParameterSet,\
    ExperimentParameter

register = Library()

def show_cc_license(value):
    """todo: document

    """

    # get cc license parameterset, if any
    schema = "http://www.tardis.edu.au/schemas" +\
    "/creative_commons/2011/05/17"

    parameterset = ExperimentParameterSet.objects.filter(
    schema__namespace=schema,
    experiment__id=value)

    from tardis.tardis_portal.ParameterSetManager import\
        ParameterSetManager

    psm = None
    if not len(parameterset):
        return "No license."
    else:
        psm = ParameterSetManager(parameterset=parameterset[0])

    image = ""
    try:
        image = psm.get_param('license_image', True)
    except ExperimentParameter.DoesNotExist:
        pass

    name = ""
    try:
        name = psm.get_param('license_name', True)
    except ExperimentParameter.DoesNotExist:
        pass

    uri = ""
    try:
        uri = psm.get_param('license_uri', True)
    except ExperimentParameter.DoesNotExist:
        pass

    if name == "":
        html = "No License."
    else:
        html = '<a href="' + uri + '"'\
        'rel="license" class="cc_js_a"><img width="88" height="31"'\
        ' border="0" class="cc_js_cc-button"'\
        'src="' + image + '"'\
        'alt="Creative Commons License"></a><br/>'\
        'This work is licensed under a <a rel="license"'\
        'href="' + uri + '">'\
        '' + name + '</a>.'

    return html

register.filter('show_cc_license', show_cc_license)
