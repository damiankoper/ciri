import {
  refDebounced,
  useGeolocation,
  useLocalStorage,
  useSpeechSynthesis,
} from '@vueuse/core';
import { v4 as uuidv4 } from 'uuid';
import { DefaultMessage } from '../models/default-message.model';
import { ErrorMessage } from '../models/error-message.model';
import { Message } from '../models/message.model';
import { MessageSerializer } from '../services/message-serializer.service';
import { axios } from '../../../plugins/axios';
import { IResponseMessage } from '../interfaces/response-message.interface';
import { ref, watch } from 'vue';
import { IRequestMessage } from '../interfaces/request-message.interface';

export function useChat() {
  const messageSerializer = new MessageSerializer();

  const { coords } = useGeolocation();
  const speechText = ref('');
  const {
    speak,
    isSupported: isSpeechSynthesisSupported,
    toggle: toogleSpeachSynthesis,
    isPlaying: isSpeechPlaying,
  } = useSpeechSynthesis(speechText);

  const isSpeechSynthesisEnabled = useLocalStorage(
    'ciri-speech-synthesis',
    false
  );

  const sender = useLocalStorage('ciri-sender', uuidv4());
  const messages = useLocalStorage<Message[]>('ciri-messages', [], {
    serializer: messageSerializer,
  });

  const isLoading = ref(false);
  const isLoadingDebounced = refDebounced(isLoading, 300);

  watch(isSpeechSynthesisEnabled, () => toogleSpeachSynthesis(false));

  async function handleRequestMessage(text: string) {
    const message = new DefaultMessage(text);
    messages.value.push(message);

    isLoading.value = true;
    try {
      const response = await axios.post<IResponseMessage[]>(
        'webhooks/rest/webhook',
        getPostPayload(text)
      );
      const transformed = messageSerializer.transformPlain(
        messageSerializer.mapResponseToPlain(response.data)
      );
      messages.value.push(...transformed);
      handleSpeech(transformed);
    } catch (e) {
      const error = new ErrorMessage('Cannot process last message');
      messages.value.push(error);
    } finally {
      isLoading.value = false;
    }
  }

  return {
    messages,
    handleRequestMessage,
    isLoadingDebounced,
    isSpeechPlaying,
    isSpeechSynthesisEnabled,
    isSpeechSynthesisSupported,
  };

  function handleSpeech(transformed: Message[]) {
    if (isSpeechSynthesisEnabled.value) {
      speechText.value = transformed.map((t) => t.getSpeech()).join('\n\n');
      speak();
    }
  }

  function getPostPayload(text: string): IRequestMessage {
    return {
      sender: sender.value,
      message: text,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      coords: {
        lat: coords.value.latitude,
        long: coords.value.longitude,
      },
    };
  }
}
