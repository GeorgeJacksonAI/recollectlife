import { useMutation } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface SendMessageDto {
  message: string;
}

interface SendMessageResponse {
  response: string;
}

// Send message to story interview endpoint
export const useSendMessage = (storyId: number | undefined) => {
  return useMutation({
    mutationFn: async (data: SendMessageDto) => {
      if (!storyId) {
        throw new Error('Story ID is required');
      }
      const response = await api.post<SendMessageResponse>(
        `/api/interview/${storyId}`,
        data
      );
      return response.data;
    },
  });
};
