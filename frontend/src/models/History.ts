
export class ConnectionHistory {
    name: string;
    events: HistoryEvent[];

    constructor( name: string, events: HistoryEvent[]) {
        this.name = name
        this.events = events
    }
}

export class HistoryEvent {
    text: string;
    editor: string;
    timestamp: Date;
    duration: number | null;
    executed: boolean;
    error: string | null;

    constructor( text: string, editor: string, timestamp: Date, duration: number | null, executed: boolean, error: string | null) {
        this.text = text
        this.editor = editor
        this.timestamp = timestamp
        this.duration = duration
        this.executed = executed
        this.error = error
    }
}