import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import ckan.logic as logic

log = logging.getLogger(__name__)


def get_organizations():
    organization_list = []
    organizations = logic.get_action('organization_list')({}, {})
    for organization_id in organizations:
        context = {'ignore_auth': True,
                   'limits': {'packages': 2},
                   'for_view': True}
        data_dict = {'id': organization_id,
                     'include_datasets': True}
        organization = logic.get_action('organization_show')(context, data_dict)
        log.debug(organization)
        organization_list.append(organization)
    return organization_list


class Welive_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'welive_theme')

    # ITemplateHelpers

    def get_helpers(self):
        return {'get_organizations': get_organizations}
