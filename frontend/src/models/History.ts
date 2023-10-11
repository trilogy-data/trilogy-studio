
export class ConnectionHistory {
    name: string;
    events: HistoryEvent[];

    constructor( name: string, events: HistoryEvent[]) {
        this.name = name
        this.events = events
    }

    // @ts-ignore
    static fromJSON({ name, events }) {
        events = events.map(dict => {
            return HistoryEvent.fromJSON(dict)
        });
        return new ConnectionHistory(name, events)
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

    static fromJSON({ text, editor, timestamp, duration, executed, error }) {
        return new HistoryEvent(text, editor, timestamp, duration, executed, error)
    }
}