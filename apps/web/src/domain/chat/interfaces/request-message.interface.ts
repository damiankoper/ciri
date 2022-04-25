export interface IRequestMessage {
  /** uuidv4 */
  sender: string;
  /** Entered text in message textarea */
  message: string;
  /** IANA Timezone id */
  timezone: string;
  /** Coords, null if permission not granted */
  metadata: {
    lat: number | null;
    long: number | null;
  };
}
