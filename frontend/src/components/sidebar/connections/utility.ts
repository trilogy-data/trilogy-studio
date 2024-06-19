



export function getConnectionExtras(type: string): Array<string> {
    if (type === 'bigquery') {
        return ['project',
            'user_or_service_auth_json']
    } else if (type === 'sql_server') {
        return [
            'host',
            'port',
            'database',
            'username',
            'password'
        ]
    }
    else if (type === 'snowflake') {
        return [
            'account',
            'username',
            'password',
        ]
    } else {
        return []
    }
}