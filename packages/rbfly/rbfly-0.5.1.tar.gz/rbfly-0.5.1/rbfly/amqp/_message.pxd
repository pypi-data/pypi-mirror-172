#
# rbfly - a library for RabbitMQ Streams using Python asyncio
#
# Copyright (C) 2021-2022 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

cdef class MessageCtx:
    """
    AMQP message context.

    :var body: Message body.
    :var annotations: Message annotations.
    :var app_properties: Application properties.
    :var stream_offset: RabbitMQ stream offset value.
    :var stream_timestamp: RabbitMQ stream offset timestamp value.
    """
    cdef:
        public object body
        public object annotations
        public object app_properties
        public int stream_offset
        public double stream_timestamp


cdef:
    struct Buffer:
        char *buffer
        Py_ssize_t size
        Py_ssize_t offset

    Py_ssize_t c_encode_amqp(char*, object) except -1
    MessageCtx c_decode_amqp(Buffer)

# vim: sw=4:et:ai
