

export enum ChatType {
    OPENAI = 'OPENAI',
}

export class ChatConnection {
    type: ChatType,
    api_key: string;
    api_secret: string;
    name: string;

    constructor( type: ChatType, api_key: string, api_secret: string, name: string) {
        this.type = type
        this.api_key = api_key
        this.api_secret = api_secret
        this.name = name
    }
}