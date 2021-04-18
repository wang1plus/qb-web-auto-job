#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:wheels
# datetime:2021/4/18 15:03
import logging
import qbittorrentapi
from datetime import datetime,timedelta
from setting import AUTO_DELETE_BEFORE_DAYS,AUTO_MOVE_BEFORE_DAYS,AUTO_MOVE_PATH

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())



def get_client() -> qbittorrentapi.Client: 
  qbt_client = qbittorrentapi.Client(host='192.168.8.106',port=9091,username='wheels',password='5m8rRfkSipzdBAS')
  try:
    qbt_client.auth_log_in()
  except qbittorrentapi.LoginFailed as e:
    logger.error(e)

  logger.debug(f'qBittorrent: {qbt_client.app.version}')
  return qbt_client


def auto_delete(qbt_client: qbittorrentapi.Client):
  # 自动删除 AUTO_DELETE_BEFORE_DAYS 天 前的 已经完成的
  infos = qbt_client.torrents_info(sorted='added_on')
  days_before = (datetime.now() - timedelta(days=AUTO_DELETE_BEFORE_DAYS))
  need_delete_hashes = []
  for item in infos:
    # pausedUP 已经下载完成 , 暂停上传
    # queuedUP 在队列中等待上传
    if item.added_on <= days_before.timestamp():
      # qbittorrentapi.TorrentStates.is_complete
      if item.state_enum.is_complete: 
        add_time = datetime.utcfromtimestamp(item.added_on).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'delete name: {item.name} ,hash: {item.hash}:  {item.state}, {add_time}')
        need_delete_hashes.append(item.hash)
  if len(need_delete_hashes) > 0:
   qbt_client.torrents.delete(hashes = need_delete_hashes,deleteFiels=None)


def move_location(qbt_client: qbittorrentapi.Client):
  # 自动移动 AUTO_MOVE_BEFORE_DAYS 天 前的 已经完成的
  infos = qbt_client.torrents_info(sorted='added_on')
  days_before = (datetime.now() - timedelta(days=AUTO_MOVE_BEFORE_DAYS))
  need_move_hashes = []
  for item in infos:
    # pausedUP 已经下载完成 , 暂停上传
    # queuedUP 在队列中等待上传
    if item.added_on <= days_before.timestamp():
      # qbittorrentapi.TorrentStates.is_complete
      if item.state_enum.is_complete: 
        if item.save_path != AUTO_MOVE_PATH:
          add_time = datetime.utcfromtimestamp(item.added_on).strftime('%Y-%m-%d %H:%M:%S')
          logger.info(f'move name: {item.name} ,hash: {item.hash}:  {item.state}, {add_time}')
          need_move_hashes.append(item.hash)

  if len(need_move_hashes) > 0 :
    qbt_client.torrents.set_location(need_move_hashes, location=AUTO_MOVE_PATH)

if __name__ == '__main__':
  qbt_client = get_client()
  auto_delete(qbt_client=qbt_client)
  move_location(qbt_client=qbt_client)