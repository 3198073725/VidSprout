import http from '../services/http'
import type { Paginated, PlaylistDetail } from './types'

const BASE = '/v1'

export function listPlaylists(): Promise<Paginated<Pick<PlaylistDetail, 'title' | 'description' | 'user' | 'media_count' | 'url' | 'thumbnail_url'>>> {
  return http.get(`${BASE}/playlists`)
}

export interface CreatePlaylistPayload {
  title: string
  description?: string
}

export function createPlaylist(payload: CreatePlaylistPayload): Promise<PlaylistDetail> {
  return http.post(`${BASE}/playlists`, payload)
}

export function getPlaylistDetail(friendlyToken: string): Promise<PlaylistDetail> {
  return http.get(`${BASE}/playlists/${friendlyToken}`)
}

export function updatePlaylist(friendlyToken: string, payload: CreatePlaylistPayload): Promise<PlaylistDetail> {
  // docs show POST for update on /playlists/{friendly_token}
  return http.post(`${BASE}/playlists/${friendlyToken}`, payload)
}

export type PlaylistMediaOp = 'add' | 'remove' | 'ordering'
export function playlistMediaOp(
  friendlyToken: string,
  body: { type: PlaylistMediaOp; media_friendly_token?: string; ordering?: number }
): Promise<{ detail: string }> {
  return http.put(`${BASE}/playlists/${friendlyToken}`, body)
}

// 添加媒体到播放列表的便捷方法
export function addMediaToPlaylist(
  playlistToken: string,
  mediaToken: string
): Promise<{ detail: string }> {
  return playlistMediaOp(playlistToken, {
    type: 'add',
    media_friendly_token: mediaToken
  })
}

// 从播放列表移除媒体的便捷方法
export function removeMediaFromPlaylist(
  playlistToken: string,
  mediaToken: string
): Promise<{ detail: string }> {
  return playlistMediaOp(playlistToken, {
    type: 'remove',
    media_friendly_token: mediaToken
  })
}

export function deletePlaylist(friendlyToken: string): Promise<void> {
  return http.delete(`${BASE}/playlists/${friendlyToken}`)
}
