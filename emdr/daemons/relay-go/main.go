package main

import (
	"fmt"
	zmq "github.com/alecthomas/gozmq"
	"github.com/bradfitz/gomemcache/memcache"
	"hash"
	"hash/fnv"
)

func main() {
	mc := memcache.New("127.0.0.1:11211")

	context, _ := zmq.NewContext()

	receiver, _ := context.NewSocket(zmq.SUB)
	receiver.SetSockOptString(zmq.SUBSCRIBE, "")
	receiver.Connect("tcp://relay-us-central-1.eve-emdr.com:8050")
	//receiver.Connect("tcp://69.147.252.42:8050")

	sender, _ := context.NewSocket(zmq.PUB)
	sender.Bind("tcp://0.0.0.0:8050")

	for {
		msg, _ := receiver.Recv(0)

		var h hash.Hash = fnv.New32()
		h.Write(msg)

		checksum := h.Sum([]byte{})
		var checksum_str string = fmt.Sprintf("%x", checksum)

		_, err := mc.Get(checksum_str)

		mc.Set(&memcache.Item{Key: checksum_str, Value: []byte{1}, Expiration: 300})

		if err == memcache.ErrCacheMiss {
			sender.Send(msg, 0)
			continue
		}

		if err == nil {
			fmt.Printf("Dupe %x\n", checksum)
		} else {
			println("Some other error")
		}

	}
}
