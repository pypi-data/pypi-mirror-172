# pyrdawos

`pyrdawos`(Python RDA AWOS)는 파이썬을 이용하여 [rdawos](https://github.com/yanghjep/rdawos)의 데이터를 조회할 수 있습니다.

조회 가능한 기상관측자료의 기간은 [rdawos](https://github.com/yanghjep/rdawos)를 따릅니다.

## 사용법

### 설치

```bash
pip install -U pyrdawos
```

### 불러오기

```python
import pyrdawos
```

### 기상관측지점 목록

```python
pyrdawos.read_stations()
```

[DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)의 헤더를 한글로 조회

```python
pyrdawos.read_stations(kor_header=True)
```

### 단일 지점의 기상관측 자료 조회

```python
pyrdawos.read_single_point('137180A001', '20210101', '20211231')
```

### 모든 지점의 기상관측 자료 조회

```python
pyrdawos.read_multi_point('20210101')
```

## 출처

> 본 저작물은 [농촌진흥청 국립농업과학원](https://www.naas.go.kr/)에서 작성하여 공공누리 제1유형으로 개방한 `농업기상관측`을 이용하였으며, 
해당 저작물은 [농업날씨365](https://weather.rda.go.kr/)에서 무료로 다운받으실 수 있습니다.
