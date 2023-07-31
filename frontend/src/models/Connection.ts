export interface ConnectionInterface {
    name: string;
    type: string;
    model: string | null;
    active: boolean;
}

export class Connection implements ConnectionInterface {

    name: string;
    type: string;
    active: boolean;
    model: string | null;

    constructor(name: string, type: string, active: boolean, model:string | null) {
        this.name = name
        this.type = type
        this.active = active || false
        this.model = model
    }
}