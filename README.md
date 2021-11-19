# bbot-ng

new generation of bbot

## Getting Started

```shell

git clone https://github.com/beiyuouo/bbot-ng.git
cd bbot-ng

# 修改bot配置文件
cp .env.dev-template .env.dev
vi .env.dev

# 修改cqhttp配置文件
cp go-cq-config/config-template.yml go-cq-config/config.yml
vi go-cq-config/config.yml

# 起飞
docker-compose up -d
```

