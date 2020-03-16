<%!
    def fmt_type(opt):
        if not isinstance(opt, dict):
            raise TypeError('options invaild')
        return opt.get('dataType', 'Object')

    def fmt_field(config):
        return '\n        '.join(['private {} {};'.format(fmt_type(field.get('options', {})), field['rename'])  for field in config['fields']])

%>
package ${ config.get('java', {}).get('dto_package', project + '.dto')};

class ${ table } {
    ${fmt_field(config)}
}
