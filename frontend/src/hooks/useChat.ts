import { useMutation, useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
    id?: number;
    story_id?: number;
    phase_context?: string;
    created_at?: string;
}

interface SendMessageDto {
    message: string;
}

interface SendMessageResponse {
    response: string;
}

// Fetch messages for a story
export const useStoryMessages = (storyId: number | undefined) => {
    return useQuery({
        queryKey: ['stories', storyId, 'messages'],
        queryFn: async () => {
            if (!storyId) {
                return [];
            }
            const response = await api.get<Message[]>(`/api/stories/${storyId}/messages`);
            return response.data;
        },
        enabled: !!storyId,
        staleTime: 30 * 1000, // 30 seconds
        refetchInterval: 5000, // Refetch every 5 seconds to get new messages
    });
};

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
