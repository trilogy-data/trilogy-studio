export enum GenAIType {
  OPENAI = "openai",
  GOOGLE = "google"
}

export class GenAIConnection {
  type: GenAIType;
  apiKey: string;
  name: string;
  active: boolean;
  extra: object | null;

  constructor(
    type: GenAIType,
    apiKey: string,
    name: string,
    active: boolean,
    extra: object | null
  ) {
    this.type = type;
    this.apiKey = apiKey;
    this.name = name;
    this.active = active || false;
    this.extra = extra;
  }

  public static fromJSON({ type, apiKey, name, active, extra }) {
    return new GenAIConnection(type, apiKey, name, active, extra);
  }
}
