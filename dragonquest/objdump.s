
dragon_quest:     file format elf64-x86-64


Disassembly of section .init:

0000000000401000 <_init>:
  401000:	f3 0f 1e fa          	endbr64
  401004:	48 83 ec 08          	sub    rsp,0x8
  401008:	48 8b 05 d1 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd1]        # 403fe0 <__gmon_start__@Base>
  40100f:	48 85 c0             	test   rax,rax
  401012:	74 02                	je     401016 <_init+0x16>
  401014:	ff d0                	call   rax
  401016:	48 83 c4 08          	add    rsp,0x8
  40101a:	c3                   	ret

Disassembly of section .plt:

0000000000401020 <.plt>:
  401020:	ff 35 ca 2f 00 00    	push   QWORD PTR [rip+0x2fca]        # 403ff0 <_GLOBAL_OFFSET_TABLE_+0x8>
  401026:	ff 25 cc 2f 00 00    	jmp    QWORD PTR [rip+0x2fcc]        # 403ff8 <_GLOBAL_OFFSET_TABLE_+0x10>
  40102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401030:	f3 0f 1e fa          	endbr64
  401034:	68 00 00 00 00       	push   0x0
  401039:	e9 e2 ff ff ff       	jmp    401020 <_init+0x20>
  40103e:	66 90                	xchg   ax,ax
  401040:	f3 0f 1e fa          	endbr64
  401044:	68 01 00 00 00       	push   0x1
  401049:	e9 d2 ff ff ff       	jmp    401020 <_init+0x20>
  40104e:	66 90                	xchg   ax,ax
  401050:	f3 0f 1e fa          	endbr64
  401054:	68 02 00 00 00       	push   0x2
  401059:	e9 c2 ff ff ff       	jmp    401020 <_init+0x20>
  40105e:	66 90                	xchg   ax,ax
  401060:	f3 0f 1e fa          	endbr64
  401064:	68 03 00 00 00       	push   0x3
  401069:	e9 b2 ff ff ff       	jmp    401020 <_init+0x20>
  40106e:	66 90                	xchg   ax,ax
  401070:	f3 0f 1e fa          	endbr64
  401074:	68 04 00 00 00       	push   0x4
  401079:	e9 a2 ff ff ff       	jmp    401020 <_init+0x20>
  40107e:	66 90                	xchg   ax,ax
  401080:	f3 0f 1e fa          	endbr64
  401084:	68 05 00 00 00       	push   0x5
  401089:	e9 92 ff ff ff       	jmp    401020 <_init+0x20>
  40108e:	66 90                	xchg   ax,ax
  401090:	f3 0f 1e fa          	endbr64
  401094:	68 06 00 00 00       	push   0x6
  401099:	e9 82 ff ff ff       	jmp    401020 <_init+0x20>
  40109e:	66 90                	xchg   ax,ax
  4010a0:	f3 0f 1e fa          	endbr64
  4010a4:	68 07 00 00 00       	push   0x7
  4010a9:	e9 72 ff ff ff       	jmp    401020 <_init+0x20>
  4010ae:	66 90                	xchg   ax,ax
  4010b0:	f3 0f 1e fa          	endbr64
  4010b4:	68 08 00 00 00       	push   0x8
  4010b9:	e9 62 ff ff ff       	jmp    401020 <_init+0x20>
  4010be:	66 90                	xchg   ax,ax
  4010c0:	f3 0f 1e fa          	endbr64
  4010c4:	68 09 00 00 00       	push   0x9
  4010c9:	e9 52 ff ff ff       	jmp    401020 <_init+0x20>
  4010ce:	66 90                	xchg   ax,ax

Disassembly of section .plt.sec:

00000000004010d0 <putchar@plt>:
  4010d0:	f3 0f 1e fa          	endbr64
  4010d4:	ff 25 26 2f 00 00    	jmp    QWORD PTR [rip+0x2f26]        # 404000 <putchar@GLIBC_2.2.5>
  4010da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000004010e0 <strncpy@plt>:
  4010e0:	f3 0f 1e fa          	endbr64
  4010e4:	ff 25 1e 2f 00 00    	jmp    QWORD PTR [rip+0x2f1e]        # 404008 <strncpy@GLIBC_2.2.5>
  4010ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000004010f0 <puts@plt>:
  4010f0:	f3 0f 1e fa          	endbr64
  4010f4:	ff 25 16 2f 00 00    	jmp    QWORD PTR [rip+0x2f16]        # 404010 <puts@GLIBC_2.2.5>
  4010fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401100 <system@plt>:
  401100:	f3 0f 1e fa          	endbr64
  401104:	ff 25 0e 2f 00 00    	jmp    QWORD PTR [rip+0x2f0e]        # 404018 <system@GLIBC_2.2.5>
  40110a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401110 <printf@plt>:
  401110:	f3 0f 1e fa          	endbr64
  401114:	ff 25 06 2f 00 00    	jmp    QWORD PTR [rip+0x2f06]        # 404020 <printf@GLIBC_2.2.5>
  40111a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401120 <getchar@plt>:
  401120:	f3 0f 1e fa          	endbr64
  401124:	ff 25 fe 2e 00 00    	jmp    QWORD PTR [rip+0x2efe]        # 404028 <getchar@GLIBC_2.2.5>
  40112a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401130 <gets@plt>:
  401130:	f3 0f 1e fa          	endbr64
  401134:	ff 25 f6 2e 00 00    	jmp    QWORD PTR [rip+0x2ef6]        # 404030 <gets@GLIBC_2.2.5>
  40113a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401140 <setvbuf@plt>:
  401140:	f3 0f 1e fa          	endbr64
  401144:	ff 25 ee 2e 00 00    	jmp    QWORD PTR [rip+0x2eee]        # 404038 <setvbuf@GLIBC_2.2.5>
  40114a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401150 <__isoc99_scanf@plt>:
  401150:	f3 0f 1e fa          	endbr64
  401154:	ff 25 e6 2e 00 00    	jmp    QWORD PTR [rip+0x2ee6]        # 404040 <__isoc99_scanf@GLIBC_2.7>
  40115a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401160 <exit@plt>:
  401160:	f3 0f 1e fa          	endbr64
  401164:	ff 25 de 2e 00 00    	jmp    QWORD PTR [rip+0x2ede]        # 404048 <exit@GLIBC_2.2.5>
  40116a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000401170 <_start>:
  401170:	f3 0f 1e fa          	endbr64
  401174:	31 ed                	xor    ebp,ebp
  401176:	49 89 d1             	mov    r9,rdx
  401179:	5e                   	pop    rsi
  40117a:	48 89 e2             	mov    rdx,rsp
  40117d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
  401181:	50                   	push   rax
  401182:	54                   	push   rsp
  401183:	45 31 c0             	xor    r8d,r8d
  401186:	31 c9                	xor    ecx,ecx
  401188:	48 c7 c7 58 1b 40 00 	mov    rdi,0x401b58
  40118f:	ff 15 43 2e 00 00    	call   QWORD PTR [rip+0x2e43]        # 403fd8 <__libc_start_main@GLIBC_2.34>
  401195:	f4                   	hlt
  401196:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  40119d:	00 00 00 

00000000004011a0 <_dl_relocate_static_pie>:
  4011a0:	f3 0f 1e fa          	endbr64
  4011a4:	c3                   	ret
  4011a5:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  4011ac:	00 00 00 
  4011af:	90                   	nop

00000000004011b0 <deregister_tm_clones>:
  4011b0:	b8 60 40 40 00       	mov    eax,0x404060
  4011b5:	48 3d 60 40 40 00    	cmp    rax,0x404060
  4011bb:	74 13                	je     4011d0 <deregister_tm_clones+0x20>
  4011bd:	b8 00 00 00 00       	mov    eax,0x0
  4011c2:	48 85 c0             	test   rax,rax
  4011c5:	74 09                	je     4011d0 <deregister_tm_clones+0x20>
  4011c7:	bf 60 40 40 00       	mov    edi,0x404060
  4011cc:	ff e0                	jmp    rax
  4011ce:	66 90                	xchg   ax,ax
  4011d0:	c3                   	ret
  4011d1:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  4011d8:	00 00 00 00 
  4011dc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

00000000004011e0 <register_tm_clones>:
  4011e0:	be 60 40 40 00       	mov    esi,0x404060
  4011e5:	48 81 ee 60 40 40 00 	sub    rsi,0x404060
  4011ec:	48 89 f0             	mov    rax,rsi
  4011ef:	48 c1 ee 3f          	shr    rsi,0x3f
  4011f3:	48 c1 f8 03          	sar    rax,0x3
  4011f7:	48 01 c6             	add    rsi,rax
  4011fa:	48 d1 fe             	sar    rsi,1
  4011fd:	74 11                	je     401210 <register_tm_clones+0x30>
  4011ff:	b8 00 00 00 00       	mov    eax,0x0
  401204:	48 85 c0             	test   rax,rax
  401207:	74 07                	je     401210 <register_tm_clones+0x30>
  401209:	bf 60 40 40 00       	mov    edi,0x404060
  40120e:	ff e0                	jmp    rax
  401210:	c3                   	ret
  401211:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401218:	00 00 00 00 
  40121c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000401220 <__do_global_dtors_aux>:
  401220:	f3 0f 1e fa          	endbr64
  401224:	80 3d 5d 2e 00 00 00 	cmp    BYTE PTR [rip+0x2e5d],0x0        # 404088 <completed.0>
  40122b:	75 13                	jne    401240 <__do_global_dtors_aux+0x20>
  40122d:	55                   	push   rbp
  40122e:	48 89 e5             	mov    rbp,rsp
  401231:	e8 7a ff ff ff       	call   4011b0 <deregister_tm_clones>
  401236:	c6 05 4b 2e 00 00 01 	mov    BYTE PTR [rip+0x2e4b],0x1        # 404088 <completed.0>
  40123d:	5d                   	pop    rbp
  40123e:	c3                   	ret
  40123f:	90                   	nop
  401240:	c3                   	ret
  401241:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401248:	00 00 00 00 
  40124c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000401250 <frame_dummy>:
  401250:	f3 0f 1e fa          	endbr64
  401254:	eb 8a                	jmp    4011e0 <register_tm_clones>

0000000000401256 <printBanner>:
  401256:	f3 0f 1e fa          	endbr64
  40125a:	55                   	push   rbp
  40125b:	48 89 e5             	mov    rbp,rsp
  40125e:	48 8d 05 a3 0d 00 00 	lea    rax,[rip+0xda3]        # 402008 <_IO_stdin_used+0x8>
  401265:	48 89 c7             	mov    rdi,rax
  401268:	e8 83 fe ff ff       	call   4010f0 <puts@plt>
  40126d:	48 8d 05 bc 0d 00 00 	lea    rax,[rip+0xdbc]        # 402030 <_IO_stdin_used+0x30>
  401274:	48 89 c7             	mov    rdi,rax
  401277:	e8 74 fe ff ff       	call   4010f0 <puts@plt>
  40127c:	48 8d 05 d5 0d 00 00 	lea    rax,[rip+0xdd5]        # 402058 <_IO_stdin_used+0x58>
  401283:	48 89 c7             	mov    rdi,rax
  401286:	e8 65 fe ff ff       	call   4010f0 <puts@plt>
  40128b:	48 8d 05 ee 0d 00 00 	lea    rax,[rip+0xdee]        # 402080 <_IO_stdin_used+0x80>
  401292:	48 89 c7             	mov    rdi,rax
  401295:	e8 56 fe ff ff       	call   4010f0 <puts@plt>
  40129a:	48 8d 05 0f 0e 00 00 	lea    rax,[rip+0xe0f]        # 4020b0 <_IO_stdin_used+0xb0>
  4012a1:	48 89 c7             	mov    rdi,rax
  4012a4:	e8 47 fe ff ff       	call   4010f0 <puts@plt>
  4012a9:	48 8d 05 40 0e 00 00 	lea    rax,[rip+0xe40]        # 4020f0 <_IO_stdin_used+0xf0>
  4012b0:	48 89 c7             	mov    rdi,rax
  4012b3:	e8 38 fe ff ff       	call   4010f0 <puts@plt>
  4012b8:	90                   	nop
  4012b9:	5d                   	pop    rbp
  4012ba:	c3                   	ret

00000000004012bb <printMenu>:
  4012bb:	f3 0f 1e fa          	endbr64
  4012bf:	55                   	push   rbp
  4012c0:	48 89 e5             	mov    rbp,rsp
  4012c3:	48 8d 05 3e 0d 00 00 	lea    rax,[rip+0xd3e]        # 402008 <_IO_stdin_used+0x8>
  4012ca:	48 89 c7             	mov    rdi,rax
  4012cd:	e8 1e fe ff ff       	call   4010f0 <puts@plt>
  4012d2:	48 8d 05 4f 0e 00 00 	lea    rax,[rip+0xe4f]        # 402128 <_IO_stdin_used+0x128>
  4012d9:	48 89 c7             	mov    rdi,rax
  4012dc:	e8 0f fe ff ff       	call   4010f0 <puts@plt>
  4012e1:	48 8d 05 70 0e 00 00 	lea    rax,[rip+0xe70]        # 402158 <_IO_stdin_used+0x158>
  4012e8:	48 89 c7             	mov    rdi,rax
  4012eb:	e8 00 fe ff ff       	call   4010f0 <puts@plt>
  4012f0:	48 8d 05 6a 0e 00 00 	lea    rax,[rip+0xe6a]        # 402161 <_IO_stdin_used+0x161>
  4012f7:	48 89 c7             	mov    rdi,rax
  4012fa:	e8 f1 fd ff ff       	call   4010f0 <puts@plt>
  4012ff:	48 8d 05 65 0e 00 00 	lea    rax,[rip+0xe65]        # 40216b <_IO_stdin_used+0x16b>
  401306:	48 89 c7             	mov    rdi,rax
  401309:	e8 e2 fd ff ff       	call   4010f0 <puts@plt>
  40130e:	48 8d 05 5e 0e 00 00 	lea    rax,[rip+0xe5e]        # 402173 <_IO_stdin_used+0x173>
  401315:	48 89 c7             	mov    rdi,rax
  401318:	e8 d3 fd ff ff       	call   4010f0 <puts@plt>
  40131d:	48 8d 05 58 0e 00 00 	lea    rax,[rip+0xe58]        # 40217c <_IO_stdin_used+0x17c>
  401324:	48 89 c7             	mov    rdi,rax
  401327:	e8 c4 fd ff ff       	call   4010f0 <puts@plt>
  40132c:	48 8d 05 54 0e 00 00 	lea    rax,[rip+0xe54]        # 402187 <_IO_stdin_used+0x187>
  401333:	48 89 c7             	mov    rdi,rax
  401336:	b8 00 00 00 00       	mov    eax,0x0
  40133b:	e8 d0 fd ff ff       	call   401110 <printf@plt>
  401340:	90                   	nop
  401341:	5d                   	pop    rbp
  401342:	c3                   	ret

0000000000401343 <learnSpell>:
  401343:	f3 0f 1e fa          	endbr64
  401347:	55                   	push   rbp
  401348:	48 89 e5             	mov    rbp,rsp
  40134b:	48 83 ec 50          	sub    rsp,0x50
  40134f:	48 89 7d c8          	mov    QWORD PTR [rbp-0x38],rdi
  401353:	48 89 75 c0          	mov    QWORD PTR [rbp-0x40],rsi
  401357:	89 55 bc             	mov    DWORD PTR [rbp-0x44],edx
  40135a:	89 4d b8             	mov    DWORD PTR [rbp-0x48],ecx
  40135d:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  401360:	3b 45 bc             	cmp    eax,DWORD PTR [rbp-0x44]
  401363:	7c 21                	jl     401386 <learnSpell+0x43>
  401365:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  401368:	89 c6                	mov    esi,eax
  40136a:	48 8d 05 1f 0e 00 00 	lea    rax,[rip+0xe1f]        # 402190 <_IO_stdin_used+0x190>
  401371:	48 89 c7             	mov    rdi,rax
  401374:	b8 00 00 00 00       	mov    eax,0x0
  401379:	e8 92 fd ff ff       	call   401110 <printf@plt>
  40137e:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  401381:	e9 b2 01 00 00       	jmp    401538 <learnSpell+0x1f5>
  401386:	c7 45 dc 00 00 00 00 	mov    DWORD PTR [rbp-0x24],0x0
  40138d:	48 8d 05 24 0e 00 00 	lea    rax,[rip+0xe24]        # 4021b8 <_IO_stdin_used+0x1b8>
  401394:	48 89 c7             	mov    rdi,rax
  401397:	e8 54 fd ff ff       	call   4010f0 <puts@plt>
  40139c:	48 8d 05 45 0e 00 00 	lea    rax,[rip+0xe45]        # 4021e8 <_IO_stdin_used+0x1e8>
  4013a3:	48 89 c7             	mov    rdi,rax
  4013a6:	b8 00 00 00 00       	mov    eax,0x0
  4013ab:	e8 60 fd ff ff       	call   401110 <printf@plt>
  4013b0:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  4013b4:	48 89 c6             	mov    rsi,rax
  4013b7:	48 8d 05 4c 0e 00 00 	lea    rax,[rip+0xe4c]        # 40220a <_IO_stdin_used+0x20a>
  4013be:	48 89 c7             	mov    rdi,rax
  4013c1:	b8 00 00 00 00       	mov    eax,0x0
  4013c6:	e8 85 fd ff ff       	call   401150 <__isoc99_scanf@plt>
  4013cb:	83 f8 01             	cmp    eax,0x1
  4013ce:	74 2c                	je     4013fc <learnSpell+0xb9>
  4013d0:	48 8d 05 39 0e 00 00 	lea    rax,[rip+0xe39]        # 402210 <_IO_stdin_used+0x210>
  4013d7:	48 89 c7             	mov    rdi,rax
  4013da:	e8 11 fd ff ff       	call   4010f0 <puts@plt>
  4013df:	90                   	nop
  4013e0:	e8 3b fd ff ff       	call   401120 <getchar@plt>
  4013e5:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
  4013e8:	83 7d f4 0a          	cmp    DWORD PTR [rbp-0xc],0xa
  4013ec:	74 06                	je     4013f4 <learnSpell+0xb1>
  4013ee:	83 7d f4 ff          	cmp    DWORD PTR [rbp-0xc],0xffffffff
  4013f2:	75 ec                	jne    4013e0 <learnSpell+0x9d>
  4013f4:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4013f7:	e9 3c 01 00 00       	jmp    401538 <learnSpell+0x1f5>
  4013fc:	48 8d 05 40 0e 00 00 	lea    rax,[rip+0xe40]        # 402243 <_IO_stdin_used+0x243>
  401403:	48 89 c7             	mov    rdi,rax
  401406:	b8 00 00 00 00       	mov    eax,0x0
  40140b:	e8 00 fd ff ff       	call   401110 <printf@plt>
  401410:	48 8d 45 dc          	lea    rax,[rbp-0x24]
  401414:	48 89 c6             	mov    rsi,rax
  401417:	48 8d 05 43 0e 00 00 	lea    rax,[rip+0xe43]        # 402261 <_IO_stdin_used+0x261>
  40141e:	48 89 c7             	mov    rdi,rax
  401421:	b8 00 00 00 00       	mov    eax,0x0
  401426:	e8 25 fd ff ff       	call   401150 <__isoc99_scanf@plt>
  40142b:	83 f8 01             	cmp    eax,0x1
  40142e:	74 2c                	je     40145c <learnSpell+0x119>
  401430:	48 8d 05 31 0e 00 00 	lea    rax,[rip+0xe31]        # 402268 <_IO_stdin_used+0x268>
  401437:	48 89 c7             	mov    rdi,rax
  40143a:	e8 b1 fc ff ff       	call   4010f0 <puts@plt>
  40143f:	90                   	nop
  401440:	e8 db fc ff ff       	call   401120 <getchar@plt>
  401445:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
  401448:	83 7d f8 0a          	cmp    DWORD PTR [rbp-0x8],0xa
  40144c:	74 06                	je     401454 <learnSpell+0x111>
  40144e:	83 7d f8 ff          	cmp    DWORD PTR [rbp-0x8],0xffffffff
  401452:	75 ec                	jne    401440 <learnSpell+0xfd>
  401454:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  401457:	e9 dc 00 00 00       	jmp    401538 <learnSpell+0x1f5>
  40145c:	90                   	nop
  40145d:	e8 be fc ff ff       	call   401120 <getchar@plt>
  401462:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
  401465:	83 7d fc 0a          	cmp    DWORD PTR [rbp-0x4],0xa
  401469:	74 06                	je     401471 <learnSpell+0x12e>
  40146b:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
  40146f:	75 ec                	jne    40145d <learnSpell+0x11a>
  401471:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401474:	85 c0                	test   eax,eax
  401476:	7e 0a                	jle    401482 <learnSpell+0x13f>
  401478:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  40147b:	3d cf 07 00 00       	cmp    eax,0x7cf
  401480:	7e 23                	jle    4014a5 <learnSpell+0x162>
  401482:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401485:	89 c6                	mov    esi,eax
  401487:	48 8d 05 2a 0e 00 00 	lea    rax,[rip+0xe2a]        # 4022b8 <_IO_stdin_used+0x2b8>
  40148e:	48 89 c7             	mov    rdi,rax
  401491:	b8 00 00 00 00       	mov    eax,0x0
  401496:	e8 75 fc ff ff       	call   401110 <printf@plt>
  40149b:	bf 01 00 00 00       	mov    edi,0x1
  4014a0:	e8 bb fc ff ff       	call   401160 <exit@plt>
  4014a5:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4014a8:	48 63 d0             	movsxd rdx,eax
  4014ab:	48 89 d0             	mov    rax,rdx
  4014ae:	48 c1 e0 02          	shl    rax,0x2
  4014b2:	48 01 d0             	add    rax,rdx
  4014b5:	48 c1 e0 02          	shl    rax,0x2
  4014b9:	48 89 c2             	mov    rdx,rax
  4014bc:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
  4014c0:	48 8d 0c 02          	lea    rcx,[rdx+rax*1]
  4014c4:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  4014c8:	ba 13 00 00 00       	mov    edx,0x13
  4014cd:	48 89 c6             	mov    rsi,rax
  4014d0:	48 89 cf             	mov    rdi,rcx
  4014d3:	e8 08 fc ff ff       	call   4010e0 <strncpy@plt>
  4014d8:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4014db:	48 63 d0             	movsxd rdx,eax
  4014de:	48 89 d0             	mov    rax,rdx
  4014e1:	48 c1 e0 02          	shl    rax,0x2
  4014e5:	48 01 d0             	add    rax,rdx
  4014e8:	48 c1 e0 02          	shl    rax,0x2
  4014ec:	48 89 c2             	mov    rdx,rax
  4014ef:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
  4014f3:	48 01 d0             	add    rax,rdx
  4014f6:	c6 40 13 00          	mov    BYTE PTR [rax+0x13],0x0
  4014fa:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4014fd:	48 98                	cdqe
  4014ff:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  401506:	00 
  401507:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
  40150b:	48 01 c2             	add    rdx,rax
  40150e:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401511:	89 02                	mov    DWORD PTR [rdx],eax
  401513:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  401517:	8b 55 dc             	mov    edx,DWORD PTR [rbp-0x24]
  40151a:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  40151e:	48 89 c6             	mov    rsi,rax
  401521:	48 8d 05 f2 0d 00 00 	lea    rax,[rip+0xdf2]        # 40231a <_IO_stdin_used+0x31a>
  401528:	48 89 c7             	mov    rdi,rax
  40152b:	b8 00 00 00 00       	mov    eax,0x0
  401530:	e8 db fb ff ff       	call   401110 <printf@plt>
  401535:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  401538:	c9                   	leave
  401539:	c3                   	ret

000000000040153a <forget>:
  40153a:	f3 0f 1e fa          	endbr64
  40153e:	55                   	push   rbp
  40153f:	48 89 e5             	mov    rbp,rsp
  401542:	48 83 ec 30          	sub    rsp,0x30
  401546:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
  40154a:	48 89 75 e0          	mov    QWORD PTR [rbp-0x20],rsi
  40154e:	89 55 dc             	mov    DWORD PTR [rbp-0x24],edx
  401551:	83 7d dc 00          	cmp    DWORD PTR [rbp-0x24],0x0
  401555:	75 17                	jne    40156e <forget+0x34>
  401557:	48 8d 05 da 0d 00 00 	lea    rax,[rip+0xdda]        # 402338 <_IO_stdin_used+0x338>
  40155e:	48 89 c7             	mov    rdi,rax
  401561:	e8 8a fb ff ff       	call   4010f0 <puts@plt>
  401566:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401569:	e9 c7 01 00 00       	jmp    401735 <forget+0x1fb>
  40156e:	c7 45 f0 ff ff ff ff 	mov    DWORD PTR [rbp-0x10],0xffffffff
  401575:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401578:	83 e8 01             	sub    eax,0x1
  40157b:	89 c6                	mov    esi,eax
  40157d:	48 8d 05 ec 0d 00 00 	lea    rax,[rip+0xdec]        # 402370 <_IO_stdin_used+0x370>
  401584:	48 89 c7             	mov    rdi,rax
  401587:	b8 00 00 00 00       	mov    eax,0x0
  40158c:	e8 7f fb ff ff       	call   401110 <printf@plt>
  401591:	48 8d 45 f0          	lea    rax,[rbp-0x10]
  401595:	48 89 c6             	mov    rsi,rax
  401598:	48 8d 05 c2 0c 00 00 	lea    rax,[rip+0xcc2]        # 402261 <_IO_stdin_used+0x261>
  40159f:	48 89 c7             	mov    rdi,rax
  4015a2:	b8 00 00 00 00       	mov    eax,0x0
  4015a7:	e8 a4 fb ff ff       	call   401150 <__isoc99_scanf@plt>
  4015ac:	83 f8 01             	cmp    eax,0x1
  4015af:	74 2c                	je     4015dd <forget+0xa3>
  4015b1:	90                   	nop
  4015b2:	e8 69 fb ff ff       	call   401120 <getchar@plt>
  4015b7:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
  4015ba:	83 7d f4 0a          	cmp    DWORD PTR [rbp-0xc],0xa
  4015be:	74 06                	je     4015c6 <forget+0x8c>
  4015c0:	83 7d f4 ff          	cmp    DWORD PTR [rbp-0xc],0xffffffff
  4015c4:	75 ec                	jne    4015b2 <forget+0x78>
  4015c6:	48 8d 05 db 0d 00 00 	lea    rax,[rip+0xddb]        # 4023a8 <_IO_stdin_used+0x3a8>
  4015cd:	48 89 c7             	mov    rdi,rax
  4015d0:	e8 1b fb ff ff       	call   4010f0 <puts@plt>
  4015d5:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  4015d8:	e9 58 01 00 00       	jmp    401735 <forget+0x1fb>
  4015dd:	90                   	nop
  4015de:	e8 3d fb ff ff       	call   401120 <getchar@plt>
  4015e3:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
  4015e6:	83 7d f8 0a          	cmp    DWORD PTR [rbp-0x8],0xa
  4015ea:	74 06                	je     4015f2 <forget+0xb8>
  4015ec:	83 7d f8 ff          	cmp    DWORD PTR [rbp-0x8],0xffffffff
  4015f0:	75 ec                	jne    4015de <forget+0xa4>
  4015f2:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
  4015f5:	85 c0                	test   eax,eax
  4015f7:	78 08                	js     401601 <forget+0xc7>
  4015f9:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
  4015fc:	39 45 dc             	cmp    DWORD PTR [rbp-0x24],eax
  4015ff:	7f 17                	jg     401618 <forget+0xde>
  401601:	48 8d 05 d0 0d 00 00 	lea    rax,[rip+0xdd0]        # 4023d8 <_IO_stdin_used+0x3d8>
  401608:	48 89 c7             	mov    rdi,rax
  40160b:	e8 e0 fa ff ff       	call   4010f0 <puts@plt>
  401610:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401613:	e9 1d 01 00 00       	jmp    401735 <forget+0x1fb>
  401618:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
  40161b:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
  40161e:	e9 a7 00 00 00       	jmp    4016ca <forget+0x190>
  401623:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401626:	48 98                	cdqe
  401628:	48 8d 50 01          	lea    rdx,[rax+0x1]
  40162c:	48 89 d0             	mov    rax,rdx
  40162f:	48 c1 e0 02          	shl    rax,0x2
  401633:	48 01 d0             	add    rax,rdx
  401636:	48 c1 e0 02          	shl    rax,0x2
  40163a:	48 89 c2             	mov    rdx,rax
  40163d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
  401641:	48 8d 0c 02          	lea    rcx,[rdx+rax*1]
  401645:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401648:	48 63 d0             	movsxd rdx,eax
  40164b:	48 89 d0             	mov    rax,rdx
  40164e:	48 c1 e0 02          	shl    rax,0x2
  401652:	48 01 d0             	add    rax,rdx
  401655:	48 c1 e0 02          	shl    rax,0x2
  401659:	48 89 c2             	mov    rdx,rax
  40165c:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
  401660:	48 01 d0             	add    rax,rdx
  401663:	ba 14 00 00 00       	mov    edx,0x14
  401668:	48 89 ce             	mov    rsi,rcx
  40166b:	48 89 c7             	mov    rdi,rax
  40166e:	e8 6d fa ff ff       	call   4010e0 <strncpy@plt>
  401673:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401676:	48 63 d0             	movsxd rdx,eax
  401679:	48 89 d0             	mov    rax,rdx
  40167c:	48 c1 e0 02          	shl    rax,0x2
  401680:	48 01 d0             	add    rax,rdx
  401683:	48 c1 e0 02          	shl    rax,0x2
  401687:	48 89 c2             	mov    rdx,rax
  40168a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
  40168e:	48 01 d0             	add    rax,rdx
  401691:	c6 40 13 00          	mov    BYTE PTR [rax+0x13],0x0
  401695:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401698:	48 98                	cdqe
  40169a:	48 83 c0 01          	add    rax,0x1
  40169e:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  4016a5:	00 
  4016a6:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
  4016aa:	48 01 d0             	add    rax,rdx
  4016ad:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
  4016b0:	48 63 d2             	movsxd rdx,edx
  4016b3:	48 8d 0c 95 00 00 00 	lea    rcx,[rdx*4+0x0]
  4016ba:	00 
  4016bb:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
  4016bf:	48 01 ca             	add    rdx,rcx
  4016c2:	8b 00                	mov    eax,DWORD PTR [rax]
  4016c4:	89 02                	mov    DWORD PTR [rdx],eax
  4016c6:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
  4016ca:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  4016cd:	83 e8 01             	sub    eax,0x1
  4016d0:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
  4016d3:	0f 8c 4a ff ff ff    	jl     401623 <forget+0xe9>
  4016d9:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  4016dc:	48 63 d0             	movsxd rdx,eax
  4016df:	48 89 d0             	mov    rax,rdx
  4016e2:	48 c1 e0 02          	shl    rax,0x2
  4016e6:	48 01 d0             	add    rax,rdx
  4016e9:	48 c1 e0 02          	shl    rax,0x2
  4016ed:	48 8d 50 ec          	lea    rdx,[rax-0x14]
  4016f1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
  4016f5:	48 01 d0             	add    rax,rdx
  4016f8:	c6 00 00             	mov    BYTE PTR [rax],0x0
  4016fb:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  4016fe:	48 98                	cdqe
  401700:	48 c1 e0 02          	shl    rax,0x2
  401704:	48 8d 50 fc          	lea    rdx,[rax-0x4]
  401708:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
  40170c:	48 01 d0             	add    rax,rdx
  40170f:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
  401715:	83 6d dc 01          	sub    DWORD PTR [rbp-0x24],0x1
  401719:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
  40171c:	89 c6                	mov    esi,eax
  40171e:	48 8d 05 e3 0c 00 00 	lea    rax,[rip+0xce3]        # 402408 <_IO_stdin_used+0x408>
  401725:	48 89 c7             	mov    rdi,rax
  401728:	b8 00 00 00 00       	mov    eax,0x0
  40172d:	e8 de f9 ff ff       	call   401110 <printf@plt>
  401732:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
  401735:	c9                   	leave
  401736:	c3                   	ret

0000000000401737 <listSpells>:
  401737:	f3 0f 1e fa          	endbr64
  40173b:	55                   	push   rbp
  40173c:	48 89 e5             	mov    rbp,rsp
  40173f:	48 83 ec 30          	sub    rsp,0x30
  401743:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
  401747:	48 89 75 e0          	mov    QWORD PTR [rbp-0x20],rsi
  40174b:	89 55 dc             	mov    DWORD PTR [rbp-0x24],edx
  40174e:	83 7d dc 00          	cmp    DWORD PTR [rbp-0x24],0x0
  401752:	75 11                	jne    401765 <listSpells+0x2e>
  401754:	48 8d 05 dd 0c 00 00 	lea    rax,[rip+0xcdd]        # 402438 <_IO_stdin_used+0x438>
  40175b:	48 89 c7             	mov    rdi,rax
  40175e:	e8 8d f9 ff ff       	call   4010f0 <puts@plt>
  401763:	eb 71                	jmp    4017d6 <listSpells+0x9f>
  401765:	48 8d 05 04 0d 00 00 	lea    rax,[rip+0xd04]        # 402470 <_IO_stdin_used+0x470>
  40176c:	48 89 c7             	mov    rdi,rax
  40176f:	e8 7c f9 ff ff       	call   4010f0 <puts@plt>
  401774:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
  40177b:	eb 51                	jmp    4017ce <listSpells+0x97>
  40177d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401780:	48 98                	cdqe
  401782:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  401789:	00 
  40178a:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
  40178e:	48 01 d0             	add    rax,rdx
  401791:	8b 08                	mov    ecx,DWORD PTR [rax]
  401793:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401796:	48 63 d0             	movsxd rdx,eax
  401799:	48 89 d0             	mov    rax,rdx
  40179c:	48 c1 e0 02          	shl    rax,0x2
  4017a0:	48 01 d0             	add    rax,rdx
  4017a3:	48 c1 e0 02          	shl    rax,0x2
  4017a7:	48 89 c2             	mov    rdx,rax
  4017aa:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
  4017ae:	48 01 c2             	add    rdx,rax
  4017b1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  4017b4:	89 c6                	mov    esi,eax
  4017b6:	48 8d 05 d2 0c 00 00 	lea    rax,[rip+0xcd2]        # 40248f <_IO_stdin_used+0x48f>
  4017bd:	48 89 c7             	mov    rdi,rax
  4017c0:	b8 00 00 00 00       	mov    eax,0x0
  4017c5:	e8 46 f9 ff ff       	call   401110 <printf@plt>
  4017ca:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
  4017ce:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  4017d1:	3b 45 dc             	cmp    eax,DWORD PTR [rbp-0x24]
  4017d4:	7c a7                	jl     40177d <listSpells+0x46>
  4017d6:	c9                   	leave
  4017d7:	c3                   	ret

00000000004017d8 <printBannerDragon>:
  4017d8:	f3 0f 1e fa          	endbr64
  4017dc:	55                   	push   rbp
  4017dd:	48 89 e5             	mov    rbp,rsp
  4017e0:	48 8d 05 21 08 00 00 	lea    rax,[rip+0x821]        # 402008 <_IO_stdin_used+0x8>
  4017e7:	48 89 c7             	mov    rdi,rax
  4017ea:	e8 01 f9 ff ff       	call   4010f0 <puts@plt>
  4017ef:	48 8d 05 b2 0c 00 00 	lea    rax,[rip+0xcb2]        # 4024a8 <_IO_stdin_used+0x4a8>
  4017f6:	48 89 c7             	mov    rdi,rax
  4017f9:	e8 f2 f8 ff ff       	call   4010f0 <puts@plt>
  4017fe:	48 8d 05 53 08 00 00 	lea    rax,[rip+0x853]        # 402058 <_IO_stdin_used+0x58>
  401805:	48 89 c7             	mov    rdi,rax
  401808:	e8 e3 f8 ff ff       	call   4010f0 <puts@plt>
  40180d:	48 8d 05 bc 0c 00 00 	lea    rax,[rip+0xcbc]        # 4024d0 <_IO_stdin_used+0x4d0>
  401814:	48 89 c7             	mov    rdi,rax
  401817:	e8 d4 f8 ff ff       	call   4010f0 <puts@plt>
  40181c:	48 8d 05 ed 0c 00 00 	lea    rax,[rip+0xced]        # 402510 <_IO_stdin_used+0x510>
  401823:	48 89 c7             	mov    rdi,rax
  401826:	e8 c5 f8 ff ff       	call   4010f0 <puts@plt>
  40182b:	90                   	nop
  40182c:	5d                   	pop    rbp
  40182d:	c3                   	ret

000000000040182e <printDragon>:
  40182e:	f3 0f 1e fa          	endbr64
  401832:	55                   	push   rbp
  401833:	48 89 e5             	mov    rbp,rsp
  401836:	48 83 ec 20          	sub    rsp,0x20
  40183a:	89 7d ec             	mov    DWORD PTR [rbp-0x14],edi
  40183d:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
  401840:	48 63 d0             	movsxd rdx,eax
  401843:	48 69 d2 d3 4d 62 10 	imul   rdx,rdx,0x10624dd3
  40184a:	48 c1 ea 20          	shr    rdx,0x20
  40184e:	89 d1                	mov    ecx,edx
  401850:	c1 f9 06             	sar    ecx,0x6
  401853:	99                   	cdq
  401854:	89 c8                	mov    eax,ecx
  401856:	29 d0                	sub    eax,edx
  401858:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
  40185b:	83 7d fc 0a          	cmp    DWORD PTR [rbp-0x4],0xa
  40185f:	7e 07                	jle    401868 <printDragon+0x3a>
  401861:	c7 45 fc 0a 00 00 00 	mov    DWORD PTR [rbp-0x4],0xa
  401868:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
  40186c:	79 07                	jns    401875 <printDragon+0x47>
  40186e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
  401875:	48 8d 05 d4 0c 00 00 	lea    rax,[rip+0xcd4]        # 402550 <_IO_stdin_used+0x550>
  40187c:	48 89 c7             	mov    rdi,rax
  40187f:	e8 6c f8 ff ff       	call   4010f0 <puts@plt>
  401884:	48 8d 05 bd 0f 00 00 	lea    rax,[rip+0xfbd]        # 402848 <_IO_stdin_used+0x848>
  40188b:	48 89 c7             	mov    rdi,rax
  40188e:	b8 00 00 00 00       	mov    eax,0x0
  401893:	e8 78 f8 ff ff       	call   401110 <printf@plt>
  401898:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
  40189f:	eb 0e                	jmp    4018af <printDragon+0x81>
  4018a1:	bf 23 00 00 00       	mov    edi,0x23
  4018a6:	e8 25 f8 ff ff       	call   4010d0 <putchar@plt>
  4018ab:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
  4018af:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
  4018b2:	3b 45 fc             	cmp    eax,DWORD PTR [rbp-0x4]
  4018b5:	7c ea                	jl     4018a1 <printDragon+0x73>
  4018b7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  4018ba:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
  4018bd:	eb 0e                	jmp    4018cd <printDragon+0x9f>
  4018bf:	bf 2d 00 00 00       	mov    edi,0x2d
  4018c4:	e8 07 f8 ff ff       	call   4010d0 <putchar@plt>
  4018c9:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
  4018cd:	83 7d f4 09          	cmp    DWORD PTR [rbp-0xc],0x9
  4018d1:	7e ec                	jle    4018bf <printDragon+0x91>
  4018d3:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
  4018d6:	89 c6                	mov    esi,eax
  4018d8:	48 8d 05 95 0f 00 00 	lea    rax,[rip+0xf95]        # 402874 <_IO_stdin_used+0x874>
  4018df:	48 89 c7             	mov    rdi,rax
  4018e2:	b8 00 00 00 00       	mov    eax,0x0
  4018e7:	e8 24 f8 ff ff       	call   401110 <printf@plt>
  4018ec:	90                   	nop
  4018ed:	c9                   	leave
  4018ee:	c3                   	ret

00000000004018ef <win>:
  4018ef:	f3 0f 1e fa          	endbr64
  4018f3:	55                   	push   rbp
  4018f4:	48 89 e5             	mov    rbp,rsp
  4018f7:	48 8d 05 7c 0f 00 00 	lea    rax,[rip+0xf7c]        # 40287a <_IO_stdin_used+0x87a>
  4018fe:	48 89 c7             	mov    rdi,rax
  401901:	e8 fa f7 ff ff       	call   401100 <system@plt>
  401906:	90                   	nop
  401907:	5d                   	pop    rbp
  401908:	c3                   	ret

0000000000401909 <lose>:
  401909:	f3 0f 1e fa          	endbr64
  40190d:	55                   	push   rbp
  40190e:	48 89 e5             	mov    rbp,rsp
  401911:	48 8d 05 70 0f 00 00 	lea    rax,[rip+0xf70]        # 402888 <_IO_stdin_used+0x888>
  401918:	48 89 c7             	mov    rdi,rax
  40191b:	e8 d0 f7 ff ff       	call   4010f0 <puts@plt>
  401920:	bf 00 00 00 00       	mov    edi,0x0
  401925:	e8 36 f8 ff ff       	call   401160 <exit@plt>

000000000040192a <fight>:
  40192a:	f3 0f 1e fa          	endbr64
  40192e:	55                   	push   rbp
  40192f:	48 89 e5             	mov    rbp,rsp
  401932:	48 83 ec 50          	sub    rsp,0x50
  401936:	48 89 7d c8          	mov    QWORD PTR [rbp-0x38],rdi
  40193a:	48 89 75 c0          	mov    QWORD PTR [rbp-0x40],rsi
  40193e:	89 55 bc             	mov    DWORD PTR [rbp-0x44],edx
  401941:	e8 92 fe ff ff       	call   4017d8 <printBannerDragon>
  401946:	83 7d bc 00          	cmp    DWORD PTR [rbp-0x44],0x0
  40194a:	75 19                	jne    401965 <fight+0x3b>
  40194c:	48 8d 05 75 0f 00 00 	lea    rax,[rip+0xf75]        # 4028c8 <_IO_stdin_used+0x8c8>
  401953:	48 89 c7             	mov    rdi,rax
  401956:	e8 95 f7 ff ff       	call   4010f0 <puts@plt>
  40195b:	bf 00 00 00 00       	mov    edi,0x0
  401960:	e8 fb f7 ff ff       	call   401160 <exit@plt>
  401965:	c7 45 fc 10 27 00 00 	mov    DWORD PTR [rbp-0x4],0x2710
  40196c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  40196f:	89 c7                	mov    edi,eax
  401971:	e8 b8 fe ff ff       	call   40182e <printDragon>
  401976:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
  40197d:	e9 94 01 00 00       	jmp    401b16 <fight+0x1ec>
  401982:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
  401985:	89 c6                	mov    esi,eax
  401987:	48 8d 05 7a 0f 00 00 	lea    rax,[rip+0xf7a]        # 402908 <_IO_stdin_used+0x908>
  40198e:	48 89 c7             	mov    rdi,rax
  401991:	b8 00 00 00 00       	mov    eax,0x0
  401996:	e8 75 f7 ff ff       	call   401110 <printf@plt>
  40199b:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
  4019a2:	eb 51                	jmp    4019f5 <fight+0xcb>
  4019a4:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
  4019a7:	48 98                	cdqe
  4019a9:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  4019b0:	00 
  4019b1:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
  4019b5:	48 01 d0             	add    rax,rdx
  4019b8:	8b 08                	mov    ecx,DWORD PTR [rax]
  4019ba:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
  4019bd:	48 63 d0             	movsxd rdx,eax
  4019c0:	48 89 d0             	mov    rax,rdx
  4019c3:	48 c1 e0 02          	shl    rax,0x2
  4019c7:	48 01 d0             	add    rax,rdx
  4019ca:	48 c1 e0 02          	shl    rax,0x2
  4019ce:	48 89 c2             	mov    rdx,rax
  4019d1:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
  4019d5:	48 01 c2             	add    rdx,rax
  4019d8:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
  4019db:	89 c6                	mov    esi,eax
  4019dd:	48 8d 05 43 0f 00 00 	lea    rax,[rip+0xf43]        # 402927 <_IO_stdin_used+0x927>
  4019e4:	48 89 c7             	mov    rdi,rax
  4019e7:	b8 00 00 00 00       	mov    eax,0x0
  4019ec:	e8 1f f7 ff ff       	call   401110 <printf@plt>
  4019f1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
  4019f5:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
  4019f8:	3b 45 bc             	cmp    eax,DWORD PTR [rbp-0x44]
  4019fb:	7c a7                	jl     4019a4 <fight+0x7a>
  4019fd:	48 8d 05 35 0f 00 00 	lea    rax,[rip+0xf35]        # 402939 <_IO_stdin_used+0x939>
  401a04:	48 89 c7             	mov    rdi,rax
  401a07:	b8 00 00 00 00       	mov    eax,0x0
  401a0c:	e8 ff f6 ff ff       	call   401110 <printf@plt>
  401a11:	c7 45 e4 ff ff ff ff 	mov    DWORD PTR [rbp-0x1c],0xffffffff
  401a18:	48 8d 45 e4          	lea    rax,[rbp-0x1c]
  401a1c:	48 89 c6             	mov    rsi,rax
  401a1f:	48 8d 05 3b 08 00 00 	lea    rax,[rip+0x83b]        # 402261 <_IO_stdin_used+0x261>
  401a26:	48 89 c7             	mov    rdi,rax
  401a29:	b8 00 00 00 00       	mov    eax,0x0
  401a2e:	e8 1d f7 ff ff       	call   401150 <__isoc99_scanf@plt>
  401a33:	83 f8 01             	cmp    eax,0x1
  401a36:	74 29                	je     401a61 <fight+0x137>
  401a38:	90                   	nop
  401a39:	e8 e2 f6 ff ff       	call   401120 <getchar@plt>
  401a3e:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
  401a41:	83 7d e8 0a          	cmp    DWORD PTR [rbp-0x18],0xa
  401a45:	74 06                	je     401a4d <fight+0x123>
  401a47:	83 7d e8 ff          	cmp    DWORD PTR [rbp-0x18],0xffffffff
  401a4b:	75 ec                	jne    401a39 <fight+0x10f>
  401a4d:	48 8d 05 f4 0e 00 00 	lea    rax,[rip+0xef4]        # 402948 <_IO_stdin_used+0x948>
  401a54:	48 89 c7             	mov    rdi,rax
  401a57:	e8 94 f6 ff ff       	call   4010f0 <puts@plt>
  401a5c:	e9 b1 00 00 00       	jmp    401b12 <fight+0x1e8>
  401a61:	90                   	nop
  401a62:	e8 b9 f6 ff ff       	call   401120 <getchar@plt>
  401a67:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
  401a6a:	83 7d f0 0a          	cmp    DWORD PTR [rbp-0x10],0xa
  401a6e:	74 06                	je     401a76 <fight+0x14c>
  401a70:	83 7d f0 ff          	cmp    DWORD PTR [rbp-0x10],0xffffffff
  401a74:	75 ec                	jne    401a62 <fight+0x138>
  401a76:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
  401a79:	85 c0                	test   eax,eax
  401a7b:	78 08                	js     401a85 <fight+0x15b>
  401a7d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
  401a80:	39 45 bc             	cmp    DWORD PTR [rbp-0x44],eax
  401a83:	7f 11                	jg     401a96 <fight+0x16c>
  401a85:	48 8d 05 ec 0e 00 00 	lea    rax,[rip+0xeec]        # 402978 <_IO_stdin_used+0x978>
  401a8c:	48 89 c7             	mov    rdi,rax
  401a8f:	e8 5c f6 ff ff       	call   4010f0 <puts@plt>
  401a94:	eb 7c                	jmp    401b12 <fight+0x1e8>
  401a96:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
  401a99:	48 98                	cdqe
  401a9b:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  401aa2:	00 
  401aa3:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
  401aa7:	48 01 d0             	add    rax,rdx
  401aaa:	8b 00                	mov    eax,DWORD PTR [rax]
  401aac:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
  401aaf:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
  401ab2:	29 45 fc             	sub    DWORD PTR [rbp-0x4],eax
  401ab5:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
  401ab9:	79 07                	jns    401ac2 <fight+0x198>
  401abb:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
  401ac2:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
  401ac5:	48 63 d0             	movsxd rdx,eax
  401ac8:	48 89 d0             	mov    rax,rdx
  401acb:	48 c1 e0 02          	shl    rax,0x2
  401acf:	48 01 d0             	add    rax,rdx
  401ad2:	48 c1 e0 02          	shl    rax,0x2
  401ad6:	48 89 c2             	mov    rdx,rax
  401ad9:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
  401add:	48 8d 0c 02          	lea    rcx,[rdx+rax*1]
  401ae1:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
  401ae4:	89 c2                	mov    edx,eax
  401ae6:	48 89 ce             	mov    rsi,rcx
  401ae9:	48 8d 05 b7 0e 00 00 	lea    rax,[rip+0xeb7]        # 4029a7 <_IO_stdin_used+0x9a7>
  401af0:	48 89 c7             	mov    rdi,rax
  401af3:	b8 00 00 00 00       	mov    eax,0x0
  401af8:	e8 13 f6 ff ff       	call   401110 <printf@plt>
  401afd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
  401b00:	89 c7                	mov    edi,eax
  401b02:	e8 27 fd ff ff       	call   40182e <printDragon>
  401b07:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
  401b0b:	75 05                	jne    401b12 <fight+0x1e8>
  401b0d:	e8 dd fd ff ff       	call   4018ef <win>
  401b12:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
  401b16:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
  401b1a:	0f 8e 62 fe ff ff    	jle    401982 <fight+0x58>
  401b20:	81 7d fc 09 0d 00 00 	cmp    DWORD PTR [rbp-0x4],0xd09
  401b27:	75 27                	jne    401b50 <fight+0x226>
  401b29:	48 8d 05 98 0e 00 00 	lea    rax,[rip+0xe98]        # 4029c8 <_IO_stdin_used+0x9c8>
  401b30:	48 89 c7             	mov    rdi,rax
  401b33:	b8 00 00 00 00       	mov    eax,0x0
  401b38:	e8 d3 f5 ff ff       	call   401110 <printf@plt>
  401b3d:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  401b41:	48 89 c7             	mov    rdi,rax
  401b44:	b8 00 00 00 00       	mov    eax,0x0
  401b49:	e8 e2 f5 ff ff       	call   401130 <gets@plt>
  401b4e:	eb 06                	jmp    401b56 <fight+0x22c>
  401b50:	e8 b4 fd ff ff       	call   401909 <lose>
  401b55:	90                   	nop
  401b56:	c9                   	leave
  401b57:	c3                   	ret

0000000000401b58 <main>:
  401b58:	f3 0f 1e fa          	endbr64
  401b5c:	55                   	push   rbp
  401b5d:	48 89 e5             	mov    rbp,rsp
  401b60:	53                   	push   rbx
  401b61:	48 83 ec 58          	sub    rsp,0x58
  401b65:	89 7d ac             	mov    DWORD PTR [rbp-0x54],edi
  401b68:	48 89 75 a0          	mov    QWORD PTR [rbp-0x60],rsi
  401b6c:	48 89 e0             	mov    rax,rsp
  401b6f:	48 89 c3             	mov    rbx,rax
  401b72:	48 8b 05 f7 24 00 00 	mov    rax,QWORD PTR [rip+0x24f7]        # 404070 <stdin@GLIBC_2.2.5>
  401b79:	b9 00 00 00 00       	mov    ecx,0x0
  401b7e:	ba 02 00 00 00       	mov    edx,0x2
  401b83:	be 00 00 00 00       	mov    esi,0x0
  401b88:	48 89 c7             	mov    rdi,rax
  401b8b:	e8 b0 f5 ff ff       	call   401140 <setvbuf@plt>
  401b90:	48 8b 05 c9 24 00 00 	mov    rax,QWORD PTR [rip+0x24c9]        # 404060 <stdout@GLIBC_2.2.5>
  401b97:	b9 00 00 00 00       	mov    ecx,0x0
  401b9c:	ba 02 00 00 00       	mov    edx,0x2
  401ba1:	be 00 00 00 00       	mov    esi,0x0
  401ba6:	48 89 c7             	mov    rdi,rax
  401ba9:	e8 92 f5 ff ff       	call   401140 <setvbuf@plt>
  401bae:	48 8b 05 cb 24 00 00 	mov    rax,QWORD PTR [rip+0x24cb]        # 404080 <stderr@GLIBC_2.2.5>
  401bb5:	b9 00 00 00 00       	mov    ecx,0x0
  401bba:	ba 02 00 00 00       	mov    edx,0x2
  401bbf:	be 00 00 00 00       	mov    esi,0x0
  401bc4:	48 89 c7             	mov    rdi,rax
  401bc7:	e8 74 f5 ff ff       	call   401140 <setvbuf@plt>
  401bcc:	e8 85 f6 ff ff       	call   401256 <printBanner>
  401bd1:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  401bd8:	c7 45 e4 0a 00 00 00 	mov    DWORD PTR [rbp-0x1c],0xa
  401bdf:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [rbp-0x14],0x0
  401be6:	8b 4d e4             	mov    ecx,DWORD PTR [rbp-0x1c]
  401be9:	48 63 c1             	movsxd rax,ecx
  401bec:	48 83 e8 01          	sub    rax,0x1
  401bf0:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
  401bf4:	48 63 c1             	movsxd rax,ecx
  401bf7:	48 89 c6             	mov    rsi,rax
  401bfa:	bf 00 00 00 00       	mov    edi,0x0
  401bff:	48 89 f0             	mov    rax,rsi
  401c02:	48 89 fa             	mov    rdx,rdi
  401c05:	48 0f a4 c2 02       	shld   rdx,rax,0x2
  401c0a:	48 c1 e0 02          	shl    rax,0x2
  401c0e:	48 01 f0             	add    rax,rsi
  401c11:	48 11 fa             	adc    rdx,rdi
  401c14:	48 0f a4 c2 05       	shld   rdx,rax,0x5
  401c19:	48 c1 e0 05          	shl    rax,0x5
  401c1d:	48 63 d1             	movsxd rdx,ecx
  401c20:	48 89 d0             	mov    rax,rdx
  401c23:	48 c1 e0 02          	shl    rax,0x2
  401c27:	48 01 d0             	add    rax,rdx
  401c2a:	48 c1 e0 02          	shl    rax,0x2
  401c2e:	48 63 c1             	movsxd rax,ecx
  401c31:	48 89 c6             	mov    rsi,rax
  401c34:	bf 00 00 00 00       	mov    edi,0x0
  401c39:	48 89 f0             	mov    rax,rsi
  401c3c:	48 89 fa             	mov    rdx,rdi
  401c3f:	48 0f a4 c2 02       	shld   rdx,rax,0x2
  401c44:	48 c1 e0 02          	shl    rax,0x2
  401c48:	48 01 f0             	add    rax,rsi
  401c4b:	48 11 fa             	adc    rdx,rdi
  401c4e:	48 0f a4 c2 05       	shld   rdx,rax,0x5
  401c53:	48 c1 e0 05          	shl    rax,0x5
  401c57:	48 63 d1             	movsxd rdx,ecx
  401c5a:	48 89 d0             	mov    rax,rdx
  401c5d:	48 c1 e0 02          	shl    rax,0x2
  401c61:	48 01 d0             	add    rax,rdx
  401c64:	48 c1 e0 02          	shl    rax,0x2
  401c68:	48 89 c2             	mov    rdx,rax
  401c6b:	b8 10 00 00 00       	mov    eax,0x10
  401c70:	48 83 e8 01          	sub    rax,0x1
  401c74:	48 01 d0             	add    rax,rdx
  401c77:	bf 10 00 00 00       	mov    edi,0x10
  401c7c:	ba 00 00 00 00       	mov    edx,0x0
  401c81:	48 f7 f7             	div    rdi
  401c84:	48 6b c0 10          	imul   rax,rax,0x10
  401c88:	48 89 c1             	mov    rcx,rax
  401c8b:	48 81 e1 00 f0 ff ff 	and    rcx,0xfffffffffffff000
  401c92:	48 89 e2             	mov    rdx,rsp
  401c95:	48 29 ca             	sub    rdx,rcx
  401c98:	48 39 d4             	cmp    rsp,rdx
  401c9b:	74 12                	je     401caf <main+0x157>
  401c9d:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
  401ca4:	48 83 8c 24 f8 0f 00 	or     QWORD PTR [rsp+0xff8],0x0
  401cab:	00 00 
  401cad:	eb e9                	jmp    401c98 <main+0x140>
  401caf:	48 89 c2             	mov    rdx,rax
  401cb2:	81 e2 ff 0f 00 00    	and    edx,0xfff
  401cb8:	48 29 d4             	sub    rsp,rdx
  401cbb:	48 89 c2             	mov    rdx,rax
  401cbe:	81 e2 ff 0f 00 00    	and    edx,0xfff
  401cc4:	48 85 d2             	test   rdx,rdx
  401cc7:	74 10                	je     401cd9 <main+0x181>
  401cc9:	25 ff 0f 00 00       	and    eax,0xfff
  401cce:	48 83 e8 08          	sub    rax,0x8
  401cd2:	48 01 e0             	add    rax,rsp
  401cd5:	48 83 08 00          	or     QWORD PTR [rax],0x0
  401cd9:	48 89 e0             	mov    rax,rsp
  401cdc:	48 83 c0 00          	add    rax,0x0
  401ce0:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
  401ce4:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
  401ce7:	48 63 d0             	movsxd rdx,eax
  401cea:	48 83 ea 01          	sub    rdx,0x1
  401cee:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  401cf2:	48 98                	cdqe
  401cf4:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  401cfb:	00 
  401cfc:	b8 10 00 00 00       	mov    eax,0x10
  401d01:	48 83 e8 01          	sub    rax,0x1
  401d05:	48 01 d0             	add    rax,rdx
  401d08:	bf 10 00 00 00       	mov    edi,0x10
  401d0d:	ba 00 00 00 00       	mov    edx,0x0
  401d12:	48 f7 f7             	div    rdi
  401d15:	48 6b c0 10          	imul   rax,rax,0x10
  401d19:	48 89 c1             	mov    rcx,rax
  401d1c:	48 81 e1 00 f0 ff ff 	and    rcx,0xfffffffffffff000
  401d23:	48 89 e2             	mov    rdx,rsp
  401d26:	48 29 ca             	sub    rdx,rcx
  401d29:	48 39 d4             	cmp    rsp,rdx
  401d2c:	74 12                	je     401d40 <main+0x1e8>
  401d2e:	48 81 ec 00 10 00 00 	sub    rsp,0x1000
  401d35:	48 83 8c 24 f8 0f 00 	or     QWORD PTR [rsp+0xff8],0x0
  401d3c:	00 00 
  401d3e:	eb e9                	jmp    401d29 <main+0x1d1>
  401d40:	48 89 c2             	mov    rdx,rax
  401d43:	81 e2 ff 0f 00 00    	and    edx,0xfff
  401d49:	48 29 d4             	sub    rsp,rdx
  401d4c:	48 89 c2             	mov    rdx,rax
  401d4f:	81 e2 ff 0f 00 00    	and    edx,0xfff
  401d55:	48 85 d2             	test   rdx,rdx
  401d58:	74 10                	je     401d6a <main+0x212>
  401d5a:	25 ff 0f 00 00       	and    eax,0xfff
  401d5f:	48 83 e8 08          	sub    rax,0x8
  401d63:	48 01 e0             	add    rax,rsp
  401d66:	48 83 08 00          	or     QWORD PTR [rax],0x0
  401d6a:	48 89 e0             	mov    rax,rsp
  401d6d:	48 83 c0 03          	add    rax,0x3
  401d71:	48 c1 e8 02          	shr    rax,0x2
  401d75:	48 c1 e0 02          	shl    rax,0x2
  401d79:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  401d7d:	c7 45 e8 00 00 00 00 	mov    DWORD PTR [rbp-0x18],0x0
  401d84:	eb 33                	jmp    401db9 <main+0x261>
  401d86:	48 8b 4d d0          	mov    rcx,QWORD PTR [rbp-0x30]
  401d8a:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
  401d8d:	48 63 d0             	movsxd rdx,eax
  401d90:	48 89 d0             	mov    rax,rdx
  401d93:	48 c1 e0 02          	shl    rax,0x2
  401d97:	48 01 d0             	add    rax,rdx
  401d9a:	48 c1 e0 02          	shl    rax,0x2
  401d9e:	48 01 c8             	add    rax,rcx
  401da1:	c6 00 00             	mov    BYTE PTR [rax],0x0
  401da4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
  401da8:	8b 55 e8             	mov    edx,DWORD PTR [rbp-0x18]
  401dab:	48 63 d2             	movsxd rdx,edx
  401dae:	c7 04 90 00 00 00 00 	mov    DWORD PTR [rax+rdx*4],0x0
  401db5:	83 45 e8 01          	add    DWORD PTR [rbp-0x18],0x1
  401db9:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
  401dbc:	3b 45 e4             	cmp    eax,DWORD PTR [rbp-0x1c]
  401dbf:	7c c5                	jl     401d86 <main+0x22e>
  401dc1:	e8 f5 f4 ff ff       	call   4012bb <printMenu>
  401dc6:	48 8d 45 b8          	lea    rax,[rbp-0x48]
  401dca:	48 89 c6             	mov    rsi,rax
  401dcd:	48 8d 05 8d 04 00 00 	lea    rax,[rip+0x48d]        # 402261 <_IO_stdin_used+0x261>
  401dd4:	48 89 c7             	mov    rdi,rax
  401dd7:	b8 00 00 00 00       	mov    eax,0x0
  401ddc:	e8 6f f3 ff ff       	call   401150 <__isoc99_scanf@plt>
  401de1:	83 f8 01             	cmp    eax,0x1
  401de4:	74 14                	je     401dfa <main+0x2a2>
  401de6:	48 8d 05 3b 0c 00 00 	lea    rax,[rip+0xc3b]        # 402a28 <_IO_stdin_used+0xa28>
  401ded:	48 89 c7             	mov    rdi,rax
  401df0:	e8 fb f2 ff ff       	call   4010f0 <puts@plt>
  401df5:	e9 e1 00 00 00       	jmp    401edb <main+0x383>
  401dfa:	90                   	nop
  401dfb:	e8 20 f3 ff ff       	call   401120 <getchar@plt>
  401e00:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  401e03:	83 7d bc 0a          	cmp    DWORD PTR [rbp-0x44],0xa
  401e07:	74 06                	je     401e0f <main+0x2b7>
  401e09:	83 7d bc ff          	cmp    DWORD PTR [rbp-0x44],0xffffffff
  401e0d:	75 ec                	jne    401dfb <main+0x2a3>
  401e0f:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  401e12:	83 f8 05             	cmp    eax,0x5
  401e15:	0f 87 a2 00 00 00    	ja     401ebd <main+0x365>
  401e1b:	89 c0                	mov    eax,eax
  401e1d:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
  401e24:	00 
  401e25:	48 8d 05 70 0c 00 00 	lea    rax,[rip+0xc70]        # 402a9c <_IO_stdin_used+0xa9c>
  401e2c:	8b 04 02             	mov    eax,DWORD PTR [rdx+rax*1]
  401e2f:	48 98                	cdqe
  401e31:	48 8d 15 64 0c 00 00 	lea    rdx,[rip+0xc64]        # 402a9c <_IO_stdin_used+0xa9c>
  401e38:	48 01 d0             	add    rax,rdx
  401e3b:	3e ff e0             	notrack jmp rax
  401e3e:	8b 4d ec             	mov    ecx,DWORD PTR [rbp-0x14]
  401e41:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
  401e44:	48 8b 75 c0          	mov    rsi,QWORD PTR [rbp-0x40]
  401e48:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
  401e4c:	48 89 c7             	mov    rdi,rax
  401e4f:	e8 ef f4 ff ff       	call   401343 <learnSpell>
  401e54:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
  401e57:	eb 7d                	jmp    401ed6 <main+0x37e>
  401e59:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
  401e5c:	48 8b 4d c0          	mov    rcx,QWORD PTR [rbp-0x40]
  401e60:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
  401e64:	48 89 ce             	mov    rsi,rcx
  401e67:	48 89 c7             	mov    rdi,rax
  401e6a:	e8 cb f6 ff ff       	call   40153a <forget>
  401e6f:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
  401e72:	eb 62                	jmp    401ed6 <main+0x37e>
  401e74:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
  401e77:	48 8b 4d c0          	mov    rcx,QWORD PTR [rbp-0x40]
  401e7b:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
  401e7f:	48 89 ce             	mov    rsi,rcx
  401e82:	48 89 c7             	mov    rdi,rax
  401e85:	e8 ad f8 ff ff       	call   401737 <listSpells>
  401e8a:	eb 4a                	jmp    401ed6 <main+0x37e>
  401e8c:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
  401e8f:	48 8b 4d c0          	mov    rcx,QWORD PTR [rbp-0x40]
  401e93:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
  401e97:	48 89 ce             	mov    rsi,rcx
  401e9a:	48 89 c7             	mov    rdi,rax
  401e9d:	e8 88 fa ff ff       	call   40192a <fight>
  401ea2:	eb 32                	jmp    401ed6 <main+0x37e>
  401ea4:	48 8d 05 a8 0b 00 00 	lea    rax,[rip+0xba8]        # 402a53 <_IO_stdin_used+0xa53>
  401eab:	48 89 c7             	mov    rdi,rax
  401eae:	e8 3d f2 ff ff       	call   4010f0 <puts@plt>
  401eb3:	bf 00 00 00 00       	mov    edi,0x0
  401eb8:	e8 a3 f2 ff ff       	call   401160 <exit@plt>
  401ebd:	48 8d 05 9c 0b 00 00 	lea    rax,[rip+0xb9c]        # 402a60 <_IO_stdin_used+0xa60>
  401ec4:	48 89 c7             	mov    rdi,rax
  401ec7:	e8 24 f2 ff ff       	call   4010f0 <puts@plt>
  401ecc:	bf 01 00 00 00       	mov    edi,0x1
  401ed1:	e8 8a f2 ff ff       	call   401160 <exit@plt>
  401ed6:	e9 e6 fe ff ff       	jmp    401dc1 <main+0x269>
  401edb:	b8 00 00 00 00       	mov    eax,0x0
  401ee0:	48 89 dc             	mov    rsp,rbx
  401ee3:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
  401ee7:	c9                   	leave
  401ee8:	c3                   	ret

Disassembly of section .fini:

0000000000401eec <_fini>:
  401eec:	f3 0f 1e fa          	endbr64
  401ef0:	48 83 ec 08          	sub    rsp,0x8
  401ef4:	48 83 c4 08          	add    rsp,0x8
  401ef8:	c3                   	ret
