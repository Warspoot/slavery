#!/bin/bash
# Rename screenshot templates to descriptive names

cd templates

# Buttons
mv Screenshot_20260217_005043.png tsugi_e_button.png 2>/dev/null || true  # 次へ
mv Screenshot_20260217_005400.png training_start_button_small.png 2>/dev/null || true  # 育成開始！ (small)
mv Screenshot_20260217_005412.png training_育成開始_button.png 2>/dev/null || true  # 育成開始！ (full)
mv Screenshot_20260217_005429.png fast_forward_icon_large.png 2>/dev/null || true  # Skip icon large
mv Screenshot_20260217_005437.png fast_forward.png 2>/dev/null || true  # Skip icon small
mv Screenshot_20260217_005450.png kettei_button.png 2>/dev/null || true  # 決定
mv Screenshot_20260217_005529.png tojiru_button.png 2>/dev/null || true  # 閉じる
mv Screenshot_20260217_005555.png omakase_button.png 2>/dev/null || true  # おまかせ
mv Screenshot_20260217_005608.png kaishi_button.png 2>/dev/null || true  # 開始
mv Screenshot_20260217_012059.png kanryou_suru_button.png 2>/dev/null || true  # 完了する
mv Screenshot_20260217_013517.png inshi_kakutei_button.png 2>/dev/null || true  # 因子確定
mv Screenshot_20260217_013627.png kakutei_button.png 2>/dev/null || true  # 確定
mv Screenshot_20260217_013704.png mouichido_button.png 2>/dev/null || true  # もう一度育成する

# Headers/banners with characters
mv Screenshot_20260217_005349.png training_start_banner.png 2>/dev/null || true  # 育成開始！with character
mv Screenshot_20260217_011645.png training_complete_button.png 2>/dev/null || true  # 育成完了！with character
mv Screenshot_20260217_012050.png kanryou_button_banner.png 2>/dev/null || true  # 完了する with character

# Headers (text only)
mv Screenshot_20260217_011555.png training_complete_header.png 2>/dev/null || true  # 育成完了！text
mv Screenshot_20260217_013458.png tsugi_e_corner.png 2>/dev/null || true  # 次へ corner

echo "Template renaming complete!"
ls -la *.png
