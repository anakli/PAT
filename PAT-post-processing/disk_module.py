#!/usr/bin/python2
#
# Copyright (c) 2015, Intel Corporation
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pat_abc import pat_base
import csv


class Disk(pat_base):
    """Contains all functions related to disk. Also contains data_array which \
    stores the data internally for further processing"""

    def __init__(self, file_path):
        """initialize disk object by parsing raw dat and storing it in a \
        structure internally"""
        self.data_array = self.get_data(file_path)
        self.time_stamp_array = []
        self.ts_sum = []
        self.avg_array_disk1 = []
        self.avg_array_disk2 = []
        self.avg_array, self.avg_array_disk1, self.avg_array_disk2 = self.extract_data()

    def extract_data(self):
        """Extract useful information from the parsed raw data and store it \
        in an array avg_array[]"""
        self.avg_array = []
        self.title_line = self.data_array[0]
        self.device_index = self.title_line.index("Device:")
        self.rps_index = self.title_line.index("r/s")
        self.wps_index = self.title_line.index("w/s")
        self.ts_index = self.title_line.index("TimeStamp")
        self.rkbps_index = self.title_line.index("rkB/s")
        self.wkbps_index = self.title_line.index("wkB/s")
        self.await_index = self.title_line.index("await")
        self.svctm_index = self.title_line.index("svctm")
        del self.data_array[0]

        self.time_stamp_array = []
        for self.row in self.data_array:
            self.time_stamp_array.append((int(self.row[self.ts_index])))

        # extract rps metric
        self.rps = []
        self.wps = []
        self.rkbps = []
        self.wkbps = []
        self.await = []
        self.svctm = []
        self.rps_disk1 = []
        self.wps_disk1 = []
        self.rkbps_disk1 = []
        self.wkbps_disk1 = []
        self.await_disk1 = []
        self.svctm_disk1 = []
        self.rps_disk2 = []
        self.wps_disk2 = []
        self.rkbps_disk2 = []
        self.wkbps_disk2 = []
        self.await_disk2 = []
        self.svctm_disk2 = []
        use_disk2 = 0
        for self.row in self.data_array:
            self.rps.append(float(self.row[self.rps_index]))
            self.wps.append(float(self.row[self.wps_index]))
            self.rkbps.append(float(self.row[self.rkbps_index]))
            self.wkbps.append(float(self.row[self.wkbps_index]))
            self.await.append(float(self.row[self.await_index]))
            self.svctm.append(float(self.row[self.svctm_index]))
            if "xvdc" in self.row[self.device_index]:
                self.rps_disk1.append(float(self.row[self.rps_index]))
                self.wps_disk1.append(float(self.row[self.wps_index]))
                self.rkbps_disk1.append(float(self.row[self.rkbps_index]))
                self.wkbps_disk1.append(float(self.row[self.wkbps_index]))
                self.await_disk1.append(float(self.row[self.await_index]))
                self.svctm_disk1.append(float(self.row[self.svctm_index]))
            elif "nvme" in self.row[self.device_index]:
                use_disk2 = 1
                self.rps_disk2.append(float(self.row[self.rps_index]))
                self.wps_disk2.append(float(self.row[self.wps_index]))
                self.rkbps_disk2.append(float(self.row[self.rkbps_index]))
                self.wkbps_disk2.append(float(self.row[self.wkbps_index]))
                self.await_disk2.append(float(self.row[self.await_index]))
                self.svctm_disk2.append(float(self.row[self.svctm_index]))


        self.ts_sum = []
        self.avg_ind = 0
        for self.index, self.row in enumerate(self.time_stamp_array):
            if (self.index != 0):
                if (self.time_stamp_array[self.index] ==
                        self.time_stamp_array[self.index-1]):
                    pass
                else:
                    self.ts_sum.append(self.time_stamp_array[self.index])
                    self.avg_ind += 1
            elif (self.index == 0):
                self.ts_sum.append(self.time_stamp_array[self.index])
        
        self.avg_array.append(self.ts_sum)

        # calculate sum writes and reads to all disks
        self.wps_sum = self.get_sum(self.wps_index, self.wps)
        self.avg_array.append(self.wps_sum)

        self.rps_sum = self.get_sum(self.rps_index, self.rps)
        self.avg_array.append(self.rps_sum)

        self.wkbps_sum = self.get_sum(self.wkbps_index, self.wkbps)
        self.avg_array.append(self.wkbps_sum)

        self.rkbps_sum = self.get_sum(self.rkbps_index, self.rkbps)
        self.avg_array.append(self.rkbps_sum)

        self.await_sum = self.get_sum(self.await_index, self.await)
        self.avg_array.append(self.await_sum)

        self.svctm_sum = self.get_sum(self.svctm_index, self.svctm)
        self.avg_array.append(self.svctm_sum)


        self.avg_array_disk1.append(self.ts_sum)

        if use_disk2 == 1:
            #calculate sum writes and reads to all disks
	    self.wps_sum = self.get_sum_for_a_disk(self.wps_index, self.wps_disk1)
	    self.avg_array_disk1.append(self.wps_sum)
	
            self.rps_sum = self.get_sum_for_a_disk(self.rps_index, self.rps_disk1)
            self.avg_array_disk1.append(self.rps_sum)

            self.wkbps_sum = self.get_sum_for_a_disk(self.wkbps_index, self.wkbps_disk1)
            self.avg_array_disk1.append(self.wkbps_sum)

            self.rkbps_sum = self.get_sum_for_a_disk(self.rkbps_index, self.rkbps_disk1)
            self.avg_array_disk1.append(self.rkbps_sum)

            self.await_sum = self.get_sum_for_a_disk(self.await_index, self.await_disk1)
            self.avg_array_disk1.append(self.await_sum)

            self.svctm_sum = self.get_sum_for_a_disk(self.svctm_index, self.svctm_disk1)
            self.avg_array_disk1.append(self.svctm_sum)


            # calculate sum writes and reads to all disks
            self.avg_array_disk2.append(self.ts_sum)
            
            self.wps_sum = self.get_sum_for_a_disk(self.wps_index, self.wps_disk2)
            self.avg_array_disk2.append(self.wps_sum)

            self.rps_sum = self.get_sum_for_a_disk(self.rps_index, self.rps_disk2)
            self.avg_array_disk2.append(self.rps_sum)

            self.wkbps_sum = self.get_sum_for_a_disk(self.wkbps_index, self.wkbps_disk2)
            self.avg_array_disk2.append(self.wkbps_sum)

            self.rkbps_sum = self.get_sum_for_a_disk(self.rkbps_index, self.rkbps_disk2)
            self.avg_array_disk2.append(self.rkbps_sum)

            self.await_sum = self.get_sum_for_a_disk(self.await_index, self.await_disk2)
            self.avg_array_disk2.append(self.await_sum)

            self.svctm_sum = self.get_sum_for_a_disk(self.svctm_index, self.svctm_disk2)
            self.avg_array_disk2.append(self.svctm_sum)


        self.data_array.insert(0, self.title_line)

        return self.avg_array, self.avg_array_disk1, self.avg_array_disk2

    def get_sum_for_a_disk(self, index, data):
        """add the reads and writes for all disks"""
        self.sum_array = []
        self.avg_ind = 0
        i = 0
    	#if len(self.time_stamp_array) > len(data[0]):
        #	self.time_stamp_array.pop() #FIXME: why is there an offset with time and data??
        for self.index, self.row in enumerate(self.time_stamp_array):
            if (self.index != 0):
                if (self.time_stamp_array[self.index] ==
                        self.time_stamp_array[self.index-1]):
                    pass
                else:
                    self.sum_array.append(data[i])
                    i += 1
        return self.sum_array

    def get_sum(self, index, data):
        """add the reads and writes for all disks"""
        self.sum_array = []
        self.avg_ind = 0
        for self.index, self.row in enumerate(self.time_stamp_array):
            if (self.index != 0):
                if (self.time_stamp_array[self.index] ==
                        self.time_stamp_array[self.index-1]):
                    self.sum_array[self.avg_ind] = self.sum_array[
                                        self.avg_ind] + data[self.index]
                else:
                    self.sum_array.append(data[self.index])
                    self.avg_ind += 1
            elif (self.index == 0):
                self.sum_array.append(data[self.index])
        return self.sum_array


def get_avg_data(cluster, name_node):
    node_count = 0
    wps_dic = {}
    rps_dic = {}
    wkbps_dic = {}
    rkbps_dic = {}
    await_dic = {}
    svctm_dic = {}
    count_dic = {}

    wps_dic1 = {}
    rps_dic1 = {}
    wkbps_dic1 = {}
    rkbps_dic1 = {}
    await_dic1 = {}
    svctm_dic1 = {}
    count_dic1 = {}

    wps_dic2 = {}
    rps_dic2 = {}
    wkbps_dic2 = {}
    rkbps_dic2 = {}
    await_dic2 = {}
    svctm_dic2 = {}
    count_dic2 = {}
    use_disk2 = False

    for node in cluster:
        if hasattr(node, 'disk_obj'):
            if node.disk_obj.data_array[1][0] != name_node:
                node_count += 1
                for index in range(len(node.disk_obj.ts_sum)-1):
                    wps = wps_dic.get(node.disk_obj.ts_sum[index])
                    if wps is not None:
                        wps += node.disk_obj.avg_array[1][index]
                        wps_dic.update(dict([(node.disk_obj.ts_sum[index],
                                       wps)]))
                        rps = rps_dic.get(node.disk_obj.ts_sum[index])
                        rps += node.disk_obj.avg_array[2][index]
                        rps_dic.update(dict([(node.disk_obj.ts_sum[index],
                                            rps)]))
                        wkbps = wkbps_dic.get(node.disk_obj.ts_sum[index])
                        wkbps += node.disk_obj.avg_array[3][index]
                        wkbps_dic.update(dict([(node.disk_obj.ts_sum[index],
                                                wkbps)]))
                        rkbps = rkbps_dic.get(node.disk_obj.ts_sum[index])
                        rkbps += node.disk_obj.avg_array[4][index]
                        rkbps_dic.update(dict([(node.disk_obj.ts_sum[index],
                                                rkbps)]))
                        await = await_dic.get(node.disk_obj.ts_sum[index])
                        await += node.disk_obj.avg_array[5][index]
                        await_dic.update(dict([(node.disk_obj.ts_sum[index],
                                                await)]))
                        svctm = svctm_dic.get(node.disk_obj.ts_sum[index])
                        svctm += node.disk_obj.avg_array[6][index]
                        svctm_dic.update(dict([(node.disk_obj.ts_sum[index],
                                                svctm)]))
                        cnt = count_dic.get(node.disk_obj.ts_sum[index])
                        cnt += 1
                        count_dic.update(dict([(node.disk_obj.ts_sum[
                            index], cnt)]))
                    else:
                        wps_dic.update(dict([(node.disk_obj.ts_sum[
                            index], node.disk_obj.avg_array[1][index])]))
                        rps_dic.update(dict([(node.disk_obj.ts_sum[
                            index], node.disk_obj.avg_array[2][index])]))
                        wkbps_dic.update(dict([(node.disk_obj.ts_sum[
                            index], node.disk_obj.avg_array[3][index])]))
                        rkbps_dic.update(dict([(node.disk_obj.ts_sum[
                            index], node.disk_obj.avg_array[4][index])]))
                        await_dic.update(dict([(node.disk_obj.ts_sum[
                            index], node.disk_obj.avg_array[5][index])]))
                        svctm_dic.update(dict([(node.disk_obj.ts_sum[
                            index], node.disk_obj.avg_array[6][index])]))
                        count_dic.update(dict([(node.disk_obj.ts_sum[
                            index], 1)]))

                    if len(node.disk_obj.avg_array_disk2) > 0:
                        #dic1
                        use_disk2 = True
                        wps = wps_dic1.get(node.disk_obj.ts_sum[index])
                        if wps is not None:
                            wps += node.disk_obj.avg_array_disk1[1][index]
                            wps_dic1.update(dict([(node.disk_obj.ts_sum[index],
                                           wps)]))
                            rps = rps_dic1.get(node.disk_obj.ts_sum[index])
                            rps += node.disk_obj.avg_array_disk1[2][index]
                            rps_dic1.update(dict([(node.disk_obj.ts_sum[index],
                                                rps)]))
                            wkbps = wkbps_dic1.get(node.disk_obj.ts_sum[index])
                            wkbps += node.disk_obj.avg_array_disk1[3][index]
                            wkbps_dic1.update(dict([(node.disk_obj.ts_sum[index],
                                                    wkbps)]))
                            rkbps = rkbps_dic1.get(node.disk_obj.ts_sum[index])
                            rkbps += node.disk_obj.avg_array_disk1[4][index]
                            rkbps_dic1.update(dict([(node.disk_obj.ts_sum[index],
                                                    rkbps)]))
                            await = await_dic1.get(node.disk_obj.ts_sum[index])
                            await += node.disk_obj.avg_array_disk1[5][index]
                            await_dic1.update(dict([(node.disk_obj.ts_sum[index],
                                                    await)]))
                            svctm = svctm_dic1.get(node.disk_obj.ts_sum[index])
                            svctm += node.disk_obj.avg_array_disk1[6][index]
                            svctm_dic1.update(dict([(node.disk_obj.ts_sum[index],
                                                    svctm)]))
                            cnt = count_dic1.get(node.disk_obj.ts_sum[index])
                            cnt += 1
                            count_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], cnt)]))
                        else:
                            wps_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk1[1][index])]))
                            rps_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk1[2][index])]))
                            wkbps_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk1[3][index])]))
                            rkbps_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk1[4][index])]))
                            await_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk1[5][index])]))
                            svctm_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk1[6][index])]))
                            count_dic1.update(dict([(node.disk_obj.ts_sum[
                                index], 1)]))

                        #dic2
                        wps = wps_dic2.get(node.disk_obj.ts_sum[index])
                        if wps is not None:
                            wps += node.disk_obj.avg_array_disk2[1][index]
                            wps_dic2.update(dict([(node.disk_obj.ts_sum[index],
                                wps)]))
                            rps = rps_dic2.get(node.disk_obj.ts_sum[index])
                            rps += node.disk_obj.avg_array_disk2[2][index]
                            rps_dic2.update(dict([(node.disk_obj.ts_sum[index],
                                rps)]))
                            wkbps = wkbps_dic2.get(node.disk_obj.ts_sum[index])
                            wkbps += node.disk_obj.avg_array_disk2[3][index]
                            wkbps_dic2.update(dict([(node.disk_obj.ts_sum[index],
                                wkbps)]))
                            rkbps = rkbps_dic2.get(node.disk_obj.ts_sum[index])
                            rkbps += node.disk_obj.avg_array_disk2[4][index]
                            rkbps_dic2.update(dict([(node.disk_obj.ts_sum[index],
                                rkbps)]))
                            await = await_dic2.get(node.disk_obj.ts_sum[index])
                            await += node.disk_obj.avg_array_disk2[5][index]
                            await_dic2.update(dict([(node.disk_obj.ts_sum[index],
                                await)]))
                            svctm = svctm_dic2.get(node.disk_obj.ts_sum[index])
                            svctm += node.disk_obj.avg_array_disk2[6][index]
                            svctm_dic2.update(dict([(node.disk_obj.ts_sum[index],
                                svctm)]))
                            cnt = count_dic2.get(node.disk_obj.ts_sum[index])
                            cnt += 1
                            count_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], cnt)]))
                        else:
                            wps_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk2[1][index])]))
                            rps_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk2[2][index])]))
                            wkbps_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk2[3][index])]))
                            rkbps_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk2[4][index])]))
                            await_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk2[5][index])]))
                            svctm_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], node.disk_obj.avg_array_disk2[6][index])]))
                            count_dic2.update(dict([(node.disk_obj.ts_sum[
                                index], 1)]))


    if node_count != 0:
        ts = rps_dic.keys()
        rps = rps_dic.values()
        wps = wps_dic.values()
        rkbps = rkbps_dic.values()
        wkbps = wkbps_dic.values()
        await = await_dic.values()
        svctm = svctm_dic.values()
        count = count_dic.values()
        rps = [x for y, x in sorted(zip(ts, rps))]
        wps = [x for y, x in sorted(zip(ts, wps))]
        rkbps = [x for y, x in sorted(zip(ts, rkbps))]
        wkbps = [x for y, x in sorted(zip(ts, wkbps))]
        await = [x for y, x in sorted(zip(ts, await))]
        svctm = [x for y, x in sorted(zip(ts, svctm))]
        count = [x for y, x in sorted(zip(ts, count))]
        ts = sorted(ts)
        
        ts1 = rps_dic1.keys()
        rps1 = rps_dic1.values()
        wps1 = wps_dic1.values()
        rkbps1 = rkbps_dic1.values()
        wkbps1 = wkbps_dic1.values()
        await1 = await_dic1.values()
        svctm1 = svctm_dic1.values()
        count1 = count_dic1.values()
        rps1 = [x for y, x in sorted(zip(ts1, rps1))]
        wps1 = [x for y, x in sorted(zip(ts1, wps1))]
        rkbps1 = [x for y, x in sorted(zip(ts1, rkbps1))]
        wkbps1 = [x for y, x in sorted(zip(ts1, wkbps1))]
        await1 = [x for y, x in sorted(zip(ts1, await1))]
        svctm1 = [x for y, x in sorted(zip(ts1, svctm1))]
        count1 = [x for y, x in sorted(zip(ts1, count1))]
        ts1 = sorted(ts1)

        if use_disk2:
            ts2 = rps_dic2.keys()
            rps2 = rps_dic2.values()
            wps2 = wps_dic2.values()
            rkbps2 = rkbps_dic2.values()
            wkbps2 = wkbps_dic2.values()
            await2 = await_dic2.values()
            svctm2 = svctm_dic2.values()
            count2 = count_dic2.values()
            rps2 = [x for y, x in sorted(zip(ts2, rps2))]
            wps2 = [x for y, x in sorted(zip(ts2, wps2))]
            rkbps2 = [x for y, x in sorted(zip(ts2, rkbps2))]
            wkbps2 = [x for y, x in sorted(zip(ts2, wkbps2))]
            await2 = [x for y, x in sorted(zip(ts2, await2))]
            svctm2 = [x for y, x in sorted(zip(ts2, svctm2))]
            count2 = [x for y, x in sorted(zip(ts2, count2))]
            ts2 = sorted(ts2)

        for index, row in enumerate(wps):
            wps[index] = row / count[index]
        for index, row in enumerate(rps):
            rps[index] = row / count[index]
        for index, row in enumerate(wkbps):
            wkbps[index] = row / count[index]
        for index, row in enumerate(rkbps):
            rkbps[index] = row / count[index]
        for index, row in enumerate(await):
            await[index] = row / count[index]
        for index, row in enumerate(svctm):
            svctm[index] = row / count[index]
        avg_array = [ts, wps, rps, wkbps, rkbps, await, svctm]

        for index, row in enumerate(wps1):
            wps1[index] = row / count1[index]
        for index, row in enumerate(rps1):
            rps1[index] = row / count1[index]
        for index, row in enumerate(wkbps1):
            wkbps1[index] = row / count1[index]
        for index, row in enumerate(rkbps1):
            rkbps1[index] = row / count1[index]
        for index, row in enumerate(await1):
            await1[index] = row / count1[index]
        for index, row in enumerate(svctm1):
            svctm1[index] = row / count1[index]
        avg_array_disk1 = [ts1, wps1, rps1, wkbps1, rkbps1, await1, svctm1]

        
        if use_disk2:
            for index, row in enumerate(wps2):
                wps2[index] = row / count2[index]
            for index, row in enumerate(rps2):
                rps2[index] = row / count2[index]
            for index, row in enumerate(wkbps2):
                wkbps2[index] = row / count2[index]
            for index, row in enumerate(rkbps2):
                rkbps2[index] = row / count2[index]
            for index, row in enumerate(await2):
                await2[index] = row / count2[index]
            for index, row in enumerate(svctm2):
                svctm2[index] = row / count2[index]
            avg_array_disk2 = [ts2, wps2, rps2, wkbps2, rkbps2, await2, svctm2]
        else:
            avg_array_disk2 = []
        return avg_array, avg_array_disk1, avg_array_disk2
    else:
        return None


# compute non-zero value average
def compute_nonzero_avg_IOPS(data):

    avg = 0
    count = 0
    for val in data:
        if val > 16:
            avg = avg + val
            count = count + 1

    if count > 0:
        avg = avg /count
    #print "Avg * count = " , avg * count

    return avg, count
    
def compute_nonzero_avg_MB(data):

    avg = 0
    count = 0
    for val in data:
        if val > 8:
            avg = avg + val
            count = count + 1

    if count > 0:
        avg = avg /count
    #print "Avg * count = " , avg * count

    return avg, count

def plot_graph2(data1, data2, pp, graph_title, result_path):
    """plot all graphs related to disk"""
    
    data1, res = get_data_for_graph(data1)
    data2, res = get_data_for_graph(data2)
    
    time_stamp_array = []
    for entry in data1[0]:
        time_stamp_array.append(float(entry))

    if len(time_stamp_array) > len(data1[1]):
        time_stamp_array.pop() #FIXME: why is there an offset with time and data??

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if res < 1:
        res = 1
    #fig_caption = "resolution - 1:" + str(res)
    fig_caption = ""
    fig.text(0.14, 0.89, fig_caption, fontsize=10,
             horizontalalignment='left', verticalalignment='top')

    x = time_stamp_array
    # plot graphs

    data1_avg_w, count = compute_nonzero_avg_IOPS(data1[1])
    data1_avg_r, count = compute_nonzero_avg_IOPS(data1[2])
    data2_avg_w, count = compute_nonzero_avg_IOPS(data2[1])
    data2_avg_r, count = compute_nonzero_avg_IOPS(data2[2])
    print "Avg wr IOPS input/output: " , data1_avg_w
    print "Avg rd IOPS input/output: " , data1_avg_r
    print "Avg wr IOPS tmp:          " , data2_avg_w
    print "Avg rd IOPS tmp:          " , data2_avg_r

    ax.plot(x, data1[1], label='input/output w/s',
            color='#800000', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data1[2], label='input/output r/s',
            color='#00297A', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data1[1], facecolor='#800000',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data1[2], rasterized=True,
                    facecolor='#00297A', alpha=0.45, linewidth=0.01)

    ax.plot(x, data2[1], label='tmp w/s',
            color='#FFA500', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data2[2], label='tmp r/s',
            color='#9ACD32', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data2[1], facecolor='#FFA500',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data2[2], rasterized=True,
                    facecolor='#9ACD32', alpha=0.45, linewidth=0.01)
    ax.legend(framealpha=0.5)
    x1, x2, y1, y2 = ax.axis()
    # set axes
    ax.axis((min(x), max(x), 0, y2))
    # set xlabel, ylabel and title
    ax.set_ylabel('requests/second')
    ax.set_xlabel('time(s)')
    ax.set_title(graph_title + ' Disk IO requests')
    ax.grid(True)
    fig.text(0.95, 0.05, pp.get_pagecount()+1, fontsize=10)
    plt.axhline(y=data1_avg_w, color='#800000', linestyle='--')
    plt.axhline(y=data1_avg_r, color='#00297A', linestyle='--')
    plt.axhline(y=data2_avg_w, color='#FFA500', linestyle='--')
    plt.axhline(y=data2_avg_r, color='#9ACD32', linestyle='--')
    pp.savefig(dpi=200)
    plt.clf()
    plt.close()

    # define new figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #fig_caption = "resolution - 1:" + str(res)
    fig_caption = ""
    fig.text(0.14, 0.89, fig_caption, fontsize=10,
             horizontalalignment='left', verticalalignment='top')
    # plot graphs
    data1[3][:] = [i / 1000 for i in data1[3]]
    data1[4][:] = [i / 1000 for i in data1[4]]
    data2[3][:] = [i / 1000 for i in data2[3]]
    data2[4][:] = [i / 1000 for i in data2[4]]
    
    data1_avg_w_mb, count1_w_mb = compute_nonzero_avg_MB(data1[3])
    data1_avg_r_mb, count1_r_mb = compute_nonzero_avg_MB(data1[4])
    data2_avg_w_mb, count2_w_mb = compute_nonzero_avg_MB(data2[3])
    data2_avg_r_mb, count2_r_mb = compute_nonzero_avg_MB(data2[4])

    print ""
    print "Avg wr MB/s input/output: " , data1_avg_w_mb
    print "Avg rd MB/s input/output: " , data1_avg_r_mb
    print "Avg wr MB/s tmp:          " , data2_avg_w_mb
    print "Avg rd MB/s tmp:          " , data2_avg_r_mb

    data1_w_mb = data1_avg_w_mb * count1_w_mb
    data1_r_mb = data1_avg_r_mb * count1_r_mb
    data2_w_mb = data2_avg_w_mb * count2_w_mb
    data2_r_mb = data2_avg_r_mb * count2_r_mb

    filename = result_path + '/disk_avg_stats.csv'
    f = open(filename, 'w')
    print >> f, data1_avg_w,',',data1_avg_r,',',data2_avg_w,',',data2_avg_r,',',data1_avg_w_mb,',',data1_avg_r_mb,',',data2_avg_w_mb,',',data2_avg_r_mb,',',data1_w_mb,',',data1_r_mb,',',data2_w_mb,',',data2_r_mb

    filename1 = result_path + '/perf.csv'
    f = open(filename1, 'w')
    approx_time = len(time_stamp_array) - 31
    print >> f, approx_time
    
    ax.plot(x, data1[3], label='input/output write MB/s',
            color='#800000', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data1[4], label='input/output read MB/s',
            color='#00297A', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data1[3], facecolor='#800000',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data1[4], rasterized=True,
                    facecolor='#00297A', alpha=0.45, linewidth=0.01)

    ax.plot(x, data2[3], label='tmp write MB/s',
            color='#FFA500', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data2[4], label='tmp read MB/s',
            color='#9ACD32', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data2[3], facecolor='#FFA500',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data2[4], rasterized=True,
                    facecolor='#9ACD32', alpha=0.45, linewidth=0.01)

    ax.legend(framealpha=0.5)
    x1, x2, y1, y2 = ax.axis()
    # set axes
    ax.axis((min(x), max(x), 0, y2))
    # set xlabel, ylabel and title
    ax.set_ylabel('Bandwidth(MB/s)')
    ax.set_xlabel('time(s)')
    ax.set_title(graph_title + ' Disk Bandwidth')
    ax.grid(True)
    fig.text(0.95, 0.05, pp.get_pagecount()+1, fontsize=10)
    plt.axhline(y=data1_avg_w_mb, color='#800000', linestyle='--')
    plt.axhline(y=data1_avg_r_mb, color='#00297A', linestyle='--')
    plt.axhline(y=data2_avg_w_mb, color='#FFA500', linestyle='--')
    plt.axhline(y=data2_avg_r_mb, color='#9ACD32', linestyle='--')
    pp.savefig(dpi=200)
    plt.clf()
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #fig_caption = "resolution - 1:" + str(res)
    fig_caption = ""
    fig.text(0.14, 0.89, fig_caption, fontsize=10,
             horizontalalignment='left', verticalalignment='top')
    # plot graphs
    ax.plot(x, data1[5], label='input/output await',
            color='#00297A', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data1[6], label='input/output svctm',
            color='#800000', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data1[5], facecolor='#00297A',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data1[6], rasterized=True,
                    facecolor='#800000', alpha=0.45, linewidth=0.01)


    ax.plot(x, data2[5], label='tmp await',
            color='#9ACD32', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data2[6], label='tmp svctm',
            color='#FFA500', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data2[5], facecolor='#9ACD32',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data2[6], rasterized=True,
                    facecolor='#FFA500', alpha=0.45, linewidth=0.01)


    ax.legend(framealpha=0.5)
    x1, x2, y1, y2 = ax.axis()
    ax.axis((min(x), max(x), 0, y2))
    ax.set_ylabel('number of requests')
    ax.set_xlabel('time(s)')
    ax.set_title(graph_title + ' Disk IO latencies')
    ax.grid(True)
    fig.text(0.95, 0.05, pp.get_pagecount()+1, fontsize=10)
    pp.savefig(dpi=200)
    plt.clf()
    plt.close()


def plot_graph(data, pp, graph_title, result_path):
    """plot all graphs related to disk"""
    
    data, res = get_data_for_graph(data)
    
    time_stamp_array = []
    for entry in data[0]:
        time_stamp_array.append(float(entry))

    if len(time_stamp_array) > len(data[1]):
        time_stamp_array.pop() #FIXME: why is there an offset with time and data??

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if res < 1:
        res = 1
    #fig_caption = "resolution - 1:" + str(res)
    fig_caption = ""
    fig.text(0.14, 0.89, fig_caption, fontsize=10,
             horizontalalignment='left', verticalalignment='top')


    # TODO: calculate average and print to file

    data_avg_w, count = compute_nonzero_avg_IOPS(data[1])
    data_avg_r, count = compute_nonzero_avg_IOPS(data[2])
    print "Avg wr IOPS total: " , data_avg_w
    print "Avg rd IOPS total: " , data_avg_r

    x = time_stamp_array
    # plot graphs

    ax.plot(x, data[1], label='w/s',
            color='#800000', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data[2], label='r/s',
            color='#00297A', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data[1], facecolor='#800000',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data[2], rasterized=True,
                    facecolor='#00297A', alpha=0.45, linewidth=0.01)
    ax.legend(framealpha=0.5)
    x1, x2, y1, y2 = ax.axis()
    # set axes
    ax.axis((min(x), max(x), 0, y2))
    # set xlabel, ylabel and title
    ax.set_ylabel('requests/second')
    ax.set_xlabel('time(s)')
    ax.set_title(graph_title + ' Disk IO requests')
    ax.grid(True)
    fig.text(0.95, 0.05, pp.get_pagecount()+1, fontsize=10)
    plt.axhline(y=data_avg_w, color='#800000', linestyle='--')
    plt.axhline(y=data_avg_r, color='#00297A', linestyle='--')
    pp.savefig(dpi=200)
    plt.clf()
    plt.close()

    # define new figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #fig_caption = "resolution - 1:" + str(res)
    fig_caption = ""
    fig.text(0.14, 0.89, fig_caption, fontsize=10,
             horizontalalignment='left', verticalalignment='top')

    data[3][:] = [i / 1000 for i in data[3]]
    data[4][:] = [i / 1000 for i in data[4]]
    data_avg_w_mb, count_w = compute_nonzero_avg_MB(data[3])
    data_avg_r_mb, count_r = compute_nonzero_avg_MB(data[4])
    print "Avg wr MB/s total: " , data_avg_w_mb
    print "Avg rd MB/s total: " , data_avg_r_mb
    
    data_w_mb = data_avg_w_mb * count_w
    data_r_mb = data_avg_r_mb * count_r
    
    filename = result_path + '/disk_avg_stats.csv'
    f = open(filename, 'w')
    print >> f, data_avg_w,',', data_avg_r,',',data_avg_w_mb,',',data_avg_r_mb,',',data_w_mb,',',data_r_mb

    filename1 = result_path + '/perf.csv'
    f = open(filename1, 'w')
    approx_time = len(time_stamp_array) - 31
    print >> f, approx_time
    
    # plot graphs
    ax.plot(x, data[3], label='write MB/s',
            color='#800000', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data[4], label='read MB/s',
            color='#00297A', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data[3], facecolor='#800000',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data[4], rasterized=True,
                    facecolor='#00297A', alpha=0.45, linewidth=0.01)

    ax.legend(framealpha=0.5)
    x1, x2, y1, y2 = ax.axis()
    # set axes
    ax.axis((min(x), max(x), 0, y2))
    # set xlabel, ylabel and title
    ax.set_ylabel('Bandwidth(MB/s)')
    ax.set_xlabel('time(s)')
    ax.set_title(graph_title + ' Disk Bandwidth')
    ax.grid(True)
    fig.text(0.95, 0.05, pp.get_pagecount()+1, fontsize=10)
    plt.axhline(y=data_avg_w_mb, color='#800000', linestyle='--')
    plt.axhline(y=data_avg_r_mb, color='#00297A', linestyle='--')
    pp.savefig(dpi=200)
    plt.clf()
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #fig_caption = "resolution - 1:" + str(res)
    fig_caption = ""
    fig.text(0.14, 0.89, fig_caption, fontsize=10,
             horizontalalignment='left', verticalalignment='top')
    # plot graphs
    ax.plot(x, data[5], label='await',
            color='#00297A', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.plot(x, data[6], label='svctm',
            color='#800000', alpha=0.9, linewidth=0.5, rasterized=True)
    ax.fill_between(x, 0, data[5], facecolor='#00297A',
                    alpha=0.45, linewidth=0.01, rasterized=True)
    ax.fill_between(x, 0, data[6], rasterized=True,
                    facecolor='#800000', alpha=0.45, linewidth=0.01)
    ax.legend(framealpha=0.5)
    x1, x2, y1, y2 = ax.axis()
    ax.axis((min(x), max(x), 0, y2))
    ax.set_ylabel('number of requests')
    ax.set_xlabel('time(s)')
    ax.set_title(graph_title + ' Disk IO latencies')
    ax.grid(True)
    fig.text(0.95, 0.05, pp.get_pagecount()+1, fontsize=10)
    pp.savefig(dpi=200)
    plt.clf()
    plt.close()

    


def get_data_for_graph(data_array):

    time_stamp_array = []
    for entry in data_array[0]:
        time_stamp_array.append(int(entry))

    x = int(round(len(time_stamp_array) / 650))
    if x > 1:
        new_ts = time_stamp_array[0::x]
        wps = []
        for entry in data_array[1]:
            wps.append(float(entry))
        new_wps = get_graph_mean(x, wps)
        rps = []
        for entry in data_array[2]:
            rps.append(float(entry))
        new_rps = get_graph_mean(x, rps)
        wkbps = []
        for entry in data_array[3]:
            wkbps.append(float(entry))
        new_wkbps = get_graph_mean(x, wkbps)
        rkbps = []
        for entry in data_array[4]:
            rkbps.append(float(entry))
        new_rkbps = get_graph_mean(x, rkbps)
        await = []
        for entry in data_array[5]:
            await.append(float(entry))
        new_await = get_graph_mean(x, await)
        svctm = []
        for entry in data_array[6]:
            svctm.append(float(entry))
        new_svctm = get_graph_mean(x, svctm)
        return [new_ts, new_wps, new_rps, new_wkbps, new_rkbps, new_await,
                new_svctm], x
    else:
        return data_array, x


def get_graph_mean(x, data):
    ind = -1
    max_val = 0
    new_data = []
    for index, entry in enumerate(data):
        if index % x == 0:
            max_val = 0
            ind += 1
            new_data.append(entry)
        else:
            max_val = max(entry, max_val)
            if max_val > new_data[ind]:
                new_data[ind] = max_val

    return new_data


def write_excel(cluster, wb):
    """create excel sheet and insert the data into the sheet"""
    ws_disk = wb.add_worksheet('disk')
    row_offset = 0
    col_offset = 0
    row_data = 0
    col_data = 0
    span = 1
    fill_value = -1
    tmp_new = []
    count = 0

    for node in cluster:
        if hasattr(node, 'disk_obj'):
            node_data = node.disk_obj.data_array
            
            tmp = [elem[1] for elem in node_data]
            variable = str(tmp[1])

            for i in tmp[2:]: #start from 3rd element in the tmp list
                  if i == variable:
                     span+=1
                  else:
                     break
            #enumerate starts from 0
            tmp_new.append('TimeStamp')
            for index,elem in enumerate(tmp[1:]):
                if index % span != 0:
                   count += 1
                else:
                   fill_value += 1
                   count = 0
                tmp_new.append(str(fill_value))

            for index, elem in enumerate(node_data):
                   elem[1] = tmp_new[index]

            tmp_new[:] = []
            span = 1

            for row in range(row_offset, (row_offset + len(node_data))):
                for col in range(col_offset,
                                 (col_offset + len(node_data[0]))):
                    if node_data[row_data][col_data].replace(
                            ".", "", 1).isdigit():
                        ws_disk.write(row, col, float(
                            node_data[row_data][col_data]))
                    else:
                        ws_disk.write(row, col, node_data[row_data][col_data])
                    col_data += 1
                col_data = 0
                row_data += 1

            row_data = 0
            row_offset = row_offset + len(node_data)

def csv_writer(cluster, csv_path_disk):  
    """write data to a CSV file path""" 

    csv_file = open(csv_path_disk, "wb")
    for node in cluster:
        if hasattr(node, 'disk_obj'):
            node_data = node.disk_obj.data_array
            for row in node_data:
                for item in row:
                    if item.replace(".", "", 1).isdigit():
                        item = float(item)        
                   
    for node in cluster:
        if hasattr(node, 'disk_obj'):
            node_data = node.disk_obj.data_array                    
              
            writer = csv.writer(csv_file, delimiter=',')
            for line in node_data:
                   writer.writerow(line)    
