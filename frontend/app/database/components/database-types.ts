// 楽曲DBの概要データ
export interface SongDataOutline {
  id: string
  title: string
}

// 楽曲DBの一覧レスポンスデータ
export interface DatabaseListResponse {
  songs: SongDataOutline[]
}

// 収録作品情報
export interface SongIncludedIn {
  type: string
  title: string
}

// 楽曲の制作背景情報
export interface SongBackground {
  description: string
  artistComment?: string | null
}

// 楽曲の音楽的特徴情報
export interface SongMusicalFeatures {
  genre: string[]
  description: string
}

// 楽曲の評価・受容情報
export interface SongReception {
  description: string
}

// 楽曲の関連情報（タイアップ、ミュージックビデオ等）
export interface SongRelatedInformation {
  type: string
  title: string
  description: string
}

// 楽曲の詳細情報
export interface SongDetails {
  background?: SongBackground | null
  musicalFeatures?: SongMusicalFeatures | null
  reception?: SongReception | null
  relatedInformation: SongRelatedInformation[]
}

// 楽曲の詳細データ
export interface SongData {
  id: string
  title: string
  artist: string
  releaseDate: string
  lyrics: string[]
  music: string[]
  includedIn: SongIncludedIn[]
  details: SongDetails
  youtubeVideoId: string[]
}
