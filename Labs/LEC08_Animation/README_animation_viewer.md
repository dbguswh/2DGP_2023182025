# Drill #8 애니메이션 뷰어

`animation_viewer.py`는 제공된 `spirtesheet.png`에서 네 가지 동작을 재생합니다.

| 동작 | 프레임 수 | 재생 속도 |
| --- | ---: | ---: |
| 대기(Idle) | 6 | 8 FPS |
| 걷기(Walk) | 10 | 10 FPS |
| 달리기(Run) | 9 | 14 FPS |
| 점프(Jump) | 14 | 12 FPS |

각 동작을 화면 중앙에서 5회 재생하고 마지막 프레임을 1초 유지합니다. 그다음 동작으로 넘어가며, 점프 후 다시 대기부터 무한 반복합니다. 캐릭터는 프레임의 종횡비를 유지하면서 높이 500픽셀로 확대합니다. 창 닫기 또는 ESC로 종료할 수 있습니다.

## 실행 및 확인

프로젝트 루트에서 실행할 경우:

```powershell
python Labs/LEC08_Animation/animation_viewer.py
python -m unittest discover -s Labs/LEC08_Animation -p test_animation_viewer.py -v
```

`sprite_sheet.png`는 원본의 사용 구간만 남기고 분홍색 배경을 투명하게 만든 재생용 이미지입니다. 이미 준비되어 있으므로 실행에 Pillow는 필요하지 않습니다. 이를 다시 생성할 때만 Pillow가 필요합니다.

```powershell
python Labs/LEC08_Animation/prepare_sprite_sheet.py
```

## 추가 기능 설명

- 프레임의 가로 크기가 서로 다른 복합 시트를 사용합니다. `frames_from_edges`가 각 프레임의 실제 좌표와 크기를 사용합니다.
- 동작별 프레임 수가 6·10·9·14개로 달라도 각각의 목록을 독립적으로 순회합니다.

원본 이미지는 사용자가 제공했습니다. 원저작자와 재배포 허락 여부는 확인되지 않았으므로 공개 배포 전 사용 권한을 확인해야 합니다.
