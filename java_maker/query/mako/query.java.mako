<%!
    def fmt_keys(config):
        return ', '.join(['"{}"'.format(field['rename']) for field in config['fields']])

    def fmt_cnname(config):
        return '\n                '.join(['put("{}", "{}");'.format(field['rename'], field['cnname'])  for field in config['fields']])

    def fmt_field(config):
        return '\n                '.join(['put("{}", "{}");'.format(field['rename'], field['field'])  for field in config['fields']])

    def fmt_jointype(val):
        if val == 'JOIN_TYPE':
            return 'EnumJoinType.LEFT_JOIN_TYPE'
        elif val == 'left join':
            return 'EnumJoinType.LEFT_JOIN_TYPE'
        elif val == 'right join':
            return 'EnumJoinType.RIGHT_JOIN_TYPE'
        elif val == 'inner join':
            return 'EnumJoinType.INNER_JOIN_TYPE'
        else:
            raise TypeError('EnumJoinType invaild {}'.format(val))

    def fmt_tables(config):
        return '\n                '.join(['add(new JoinTable("{}", "{}", {}, "{}"));'.format(
            field['field'], field['rename'], fmt_jointype(field['join']), field['on']
        )  for field in config['tables'] if field['join'] != 'master'])

    def get_master(config):
        master = list(filter(lambda x: x['join'] == 'master', config['tables']))
        if len(master) > 1:
            raise TypeError('tables master too many')

        master = master[0]
        return master
%>
package ${ config.get('java', {}).get('query_package', project + '.query')};


import java.util.*;

import ${ config.get('java', {}).get('queryhelp_package', project + '.queryhelp')}.QueryMakerImpl;
import ${ config.get('java', {}).get('queryhelp_package', project + '.queryhelp')}.enums.EnumJoinType;
import ${ config.get('java', {}).get('queryhelp_package', project + '.queryhelp')}.params.FieldDefineMap;
import ${ config.get('java', {}).get('queryhelp_package', project + '.queryhelp')}.sqlmaker.impl.JoinTable;

public class ${ table } extends QueryMakerImpl {


    public ${ table }(){
        super(
            "${get_master(config)['field']}", 
            "${get_master(config)['rename']}", 
            new HashSet<String>(Arrays.asList(${fmt_keys(config)})), 
            new FieldDefineMap(){{
                ${fmt_cnname(config)}
            }}, 
            new FieldDefineMap(){{
                ${fmt_field(config)}
            }}, 
            new ArrayList<JoinTable>(){{
                ${fmt_tables(config)}
            }}
        );
    }
}
