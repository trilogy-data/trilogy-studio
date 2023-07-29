export interface ConnectionInterface {
    name: string;
    type: string;
    active: boolean;
}

export class Connection implements ConnectionInterface {

    name: string;
    type: string;
    active: boolean;

    constructor(name: string, type: string, active: boolean) {
        this.name = name
        this.type = type
        this.active = active || false
    }
}