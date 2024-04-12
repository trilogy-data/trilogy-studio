import { GenAIType } from "/src/models/GenAIConnection";

export function getConnectionExtras(type: GenAIType): Array<string> {
  if (type === GenAIType.OPENAI) {
    return ["model"];
  } else {
    return [];
  }
}
