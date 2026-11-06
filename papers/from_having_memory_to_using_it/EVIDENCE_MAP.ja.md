# Evidence map — From Having Memory to Using It

v1.2 — 2026-11-06。詳細骨子の付録Bを抜き出した編集用資料。

## Appendix B. Evidence map and writing rules

**主張：** 主張の強さは、実験の単位・事前指定の範囲・公開された証拠に合わせる。

**使う証拠：** 固定コミットの参照と取得した原文を `sources/manifest.json` に保存した。E7-DとMC-5Cの主要数値は保存集計を確認。OTB21は全保存記録の主要項目を再集計して一致を確認。MC-4X、MC-5D、OTB20、OTB22、E3bの引用は報告に基づく。これら既存系列の計算軌道全体を再実行したとは記載しない。追加した履歴寄与実験の一次集計・報告・凍結記録は `sources/history_coupling_manifest.json` に別保存した。pilot240軌道、先行評価96軌道は同一作業内の別実装で照合した。新20回路の一次集計・計画・監査は `sources/wrong_history_manifest.json` で結果コミット `bed5dc0` へ固定した。320保存評価ファイルの別採点、192軌道と128自前/ドナー境界のscalar照合を確認した。入力ハッシュは今回は生成時点で保存した。過去cohort監査の利用可能な記録範囲も明示され、全リモート履歴の保証には拡張しない [WH-AUDIT] [WH-DYNAMICS]。

**想定される反論：** 「監査済みなら独立追試と同じでは」。同一プロジェクト内の別コードによる集計照合、元コードの再実行、別実装の軌道照合、外部研究者の追試を別欄にする。公開報告があることと、完全な再実行パッケージがあることも区別する。

| 証拠 | 本稿で使う分類 | 本稿で支えるもの | 主張しないもの |
|---|---|---|---|
| MC-4X | 探索・5回路 | 保持と下流利用の差、読出し時間の問題 | 普遍的な時定数則、T7優位 |
| E7-D | 固定5回路の未使用入力での確証。失敗分解は記述分析 | 読み出しに基づく選択の改善、候補集合の制約 | 新回路への一般化、自己学習 |
| 履歴寄与pilot | 既知5回路の探索 | 方策依存の逆転という仮説、移植救済の未確認 | 知能の同定、一般的な履歴の必要性 |
| 履歴寄与新評価 | 取得前解析固定・外部事前登録なし。最小効果基準未達、副解析は記述的 | 条件つき正差、同じ回路・方策での別入力群における符号反転 | 全回路一貫性、新回路一般化、最小効果の確立、C3救済 |
| 新回路P1 | 取得前固定、訓練pilotとは別20回路。回路推論、5検定Holm族 | 同一生成・回路別較正・訓練手順で通常−除去の平均正差 | 先行3pt基準の救済、全回路一貫性、他課題・任意の回路への一般化 |
| 新回路P2・通常−ドナー | 同じ主検定族で正差を支持。A・現在入力を対応 | 自前の境界成分がこの対応ドナーより良い、という条件つき比較 | 純粋な意味内容の同定、動作点／状態適合性の完全排除 |
| 新回路P2・ドナー−除去／等価 | 悪化・両等価性とも未達。±2ptは取得前固定 | 何を未判定として残すか | 無効果、等価、ドナーの利益、有意な4条件の完全順位 |
| 新回路・固定方策／A別／保持 | 事前指定の記述的副次 | 固定方策の逆転を再観測、A=1の正差、保持順序の反転 | 無条件の安定則、A=0の負差の確立、長い保持ほど有利という法則 |
| 新回路・Bconst／直後1回 | 事前指定の記述的副次 | 固定値の対照と複数の時間範囲を測る必要 | 時間変動だけの効果、直後の等価性、軌道による媒介の同定 |
| MC-5C | 未使用20回路の確証。T7比較は副次 | 特定課題での役割分担、T7中継の不利 | T7記憶群の優位、発火率一致比較 |
| MC-5D | 別5回路の探索 | 発火率を近づけても残る中継の不利 | 全動作点での劣位、機構の完全特定 |
| E3b | 予備実験後に固定した評価手順の報告 | 学習可能な更新則による別の解法 | 公平なT7/GRU性能順位、GRU学習成功率の一般化 |
| OTB20 | 探索 | 保護と獲得を両方測る必要 | 誤差制限一般の無効性 |
| OTB21 | 固定方策の新位相・期限での境界評価 | 指定範囲での獲得・保持、追加時間 | 同時間優位、自律guard、自然履歴への一般化 |
| OTB22 | pilot後の取得前固定の機構試験、記述分析 | 接続中の共同利用と遮断対照 | 受け手学習、矛盾解決、実通信での実証 |

### B.1 新結果を本文へ移すときの言い換え

|過剰になり得る表現|本稿で使う表現|根拠・未分離事項|
|---|---|---|
|「動作点では説明できない」|「周辺の大きさを近づけても、自前と対応ドナーに差が残った」|位相等との同時分布・適合性は一致していない|
|「変動する過去そのものに価値がある」|「減衰ドナーは持続定数より高い成績だった（副次）」|時間形・累積入力も変わる|
|「履歴の残差だけを入れ替えた」|「同じA・現在入力に対応づけた、別履歴群の成分へ差し替えた」|統計的残差化を実施したわけではない|
|「直後には効かず、軌道形成で効く」|「直後の点推定は小さく、7回の連鎖では正差を支持。機構は未同定」|直後の区間は約±3pt、等価性・媒介は未検証|
|「A=1だけに安定して効く」|「A=1の正差を再観測し、A=0の負差は確立しなかった」|群ごとの有意性の違いは群間差や排他性の証明ではない|

主張・数値・分類・一次資料の対応は本文末の参照と `sources/wrong_history_manifest.json` に残す。新たな試験や取得を行わず、保存結果の引用・編集として反映する。

**元骨子から今回採用しない数値・表現：**

- 読み出しの「4→64素子、78.4%→94.1%、上限約96%」は、今回その定義と元集計を照合していないため使わない。確証の93.8%等と混ぜない。
- 「選択失敗1.8%」を条件付きの誤選択率として使わない。E7-Dの保存集計では、成功候補がある場合と全判断に対する指標が別である。本稿の中心例には分母が明確な失敗内訳を採用する。
- 「最軽量クラス」「他人が真似できない」「単位が増えても質的跳躍は起きない」「LIFは履歴を持たない」は使わない。
- OTB0〜4・OTB13を個別の実証根拠として追加する場合は、その版・構成・結果を別途照合する。動詞に番号を機械的に割り当てない。

[MODEL]: https://github.com/type37c/oscillator-mind/blob/master/docs/INDIVIDUAL_DYNAMICS.md
[MC4X]: https://github.com/type37c/oscillator-arithmetic/blob/045756c15a1f7d1acce20c89fabfacb23870398d/experiments/mc4_memory_to_computation/MC4X_REPORT.md
[MC5C]: https://github.com/type37c/oscillator-arithmetic/blob/045756c15a1f7d1acce20c89fabfacb23870398d/experiments/mc5c_relay_confirm/MC5C_REPORT.md
[MC5CDATA]: https://github.com/type37c/oscillator-arithmetic/blob/045756c15a1f7d1acce20c89fabfacb23870398d/results/mc5c_relay_confirm/verdicts.json
[MC5D]: https://github.com/type37c/oscillator-arithmetic/blob/045756c15a1f7d1acce20c89fabfacb23870398d/experiments/mc5d_relay_diagnosis/MC5D_REPORT.md
[E3B]: https://github.com/type37c/oscillator-arithmetic/blob/045756c15a1f7d1acce20c89fabfacb23870398d/experiments/e3b_gru_training/E3B_REPORT.md
[E7D]: https://github.com/type37c/oscillator-arithmetic/blob/01d84b5a41cc8d521724bbaa0127601b086b9936/experiments/e7d_confirm/E7DCF_REPORT.md
[E7PLAN]: https://github.com/type37c/oscillator-arithmetic/blob/01d84b5a41cc8d521724bbaa0127601b086b9936/experiments/e7d_confirm/PLAN.md
[E7RESULTS]: https://github.com/type37c/oscillator-arithmetic/blob/01d84b5a41cc8d521724bbaa0127601b086b9936/results/e7d_confirm/results.json
[OTB20]: https://github.com/type37c/oscillator-arithmetic/blob/e3a5e1e66eae794a7fd56bae5f4d5054a74528c2/results/otb20_bounded_error_amplification/REPORT.md
[OTB21]: https://github.com/type37c/oscillator-mind/blob/1c70be3bc7df1bce568e6dc102dde7a573e00597/results/otb21_readiness_history_validation/REPORT.md
[OTB22]: https://github.com/type37c/oscillator-arithmetic/blob/e3a5e1e66eae794a7fd56bae5f4d5054a74528c2/results/otb22_shared_experience_network/REPORT.md

追加実験の参照は、未pushのローカル資産である。投稿時には公開可能な固定版へのリンクへ置換する。架空のGitHub公開URLは作らない。

[HC-PILOT]: sources/HISTORY_COUPLING_PILOT_REPORT.ja.md
[HC-REPORT]: sources/HISTORY_COUPLING_CONFIRMATION_REPORT.ja.md
[HC-DATA]: sources/HISTORY_COUPLING_CONFIRMATION_summary.json
[HC-PLAN]: sources/HISTORY_COUPLING_CONFIRMATION_PROTOCOL.ja.md
[HC-FREEZE]: sources/HISTORY_COUPLING_CONFIRMATION_FREEZE.json

[HC-CODE]: sources/HISTORY_COUPLING_PILOT_CODE.py

[WH-DATA]: sources/WH_analysis.json
[WH-PLAN]: sources/WH_PLAN.md
[WH-FREEZE]: sources/WH_FREEZE.json
[WH-REPORT]: sources/WH_REPORT.ja.md
[WH-AUDIT]: sources/WH_saved_data_audit.json
[WH-DYNAMICS]: sources/WH_dynamics_audit.json
