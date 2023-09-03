



export function getConnectionExtras(type:string): Array<string> {
    if (type === 'bigquery') {
        return ['project']
    } else if (type === 'sql_server') {
        return [
            'host',
            'port',
            'database',
            'username',
            'password'
        ]

        // {
        //     host: '',
        //     port: '',
        //     database: '',
        //     username: '',
        //     password: '',
        // }
    } else {
        return []
    }
}